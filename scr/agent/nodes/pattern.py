from errno import EXDEV
from langchain_core.runnables import RunnableConfig
from scr.agent.state.state import State, StepOutput
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Any
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from scr.agent.utils.config import Configuration
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from scr.agent.prompts.prompts import SWISSLIPIDS_DESCRIPTION_QUERY, UNIPROT_DESCRIPTION_QUERY, RHEA_DESCRIPTION_QUERY, QUERY_PATTERN_PROMPT_PRIMARY_BLOCK, QUERY_PATTERN_PROMPT_SERVICE_BLOCK
import os
import pathlib
import logging
from scr.agent.state.state import QueryPlan, QueryState, Candidate
from scr.agent.utils.llm_utils import get_llm
from entity_indexing.endpoint_loader import query_sparql_wrapper
from experiments.utilities.sparql_syntax_validation import validate_sparql_syntax



max_attempts = 3


async def generate_and_validate_blocks(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:


    configuration = Configuration.from_runnable_config(config)



    try:
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model").with_structured_output(schema = Candidate)


        prompt_template_service = PromptTemplate(
            template=QUERY_PATTERN_PROMPT_SERVICE_BLOCK,
            input_variables=["input", "target_endpoint", "extracted_example_queries", "endpoint_description", "failed_pattern", "iri_mapping", "service_endpoint"],
            template_format="jinja2"
        )

        prompt_template_primary = PromptTemplate(
            template=QUERY_PATTERN_PROMPT_PRIMARY_BLOCK,
            input_variables=["input", "target_endpoint", "extracted_example_queries", "endpoint_description", "failed_pattern", "iri_mapping"],
            template_format="jinja2"
        )

        for block in state.query_state.blocks:

            if(block.attempt > max_attempts):
                continue
            

            while block.attempt < max_attempts:
                
                description = ""
                
                if block.endpoint == block.target_endpoint:
                    if block.endpoint == "https://sparql.swisslipids.org/sparql/":
                        description = SWISSLIPIDS_DESCRIPTION_QUERY
                    elif block.endpoint == "https://sparql.uniprot.org/sparql":
                        description = UNIPROT_DESCRIPTION_QUERY
                    elif block.endpoint == "https://sparql.rhea-db.org/sparql":
                        description = RHEA_DESCRIPTION_QUERY
                    else:
                        description = ""
                else:
                    if block.endpoint == "https://sparql.swisslipids.org/sparql/":
                        description = SWISSLIPIDS_DESCRIPTION_QUERY
                    elif block.endpoint == "https://sparql.uniprot.org/sparql":
                        description = UNIPROT_DESCRIPTION_QUERY
                    elif block.endpoint == "https://sparql.rhea-db.org/sparql":
                        description = RHEA_DESCRIPTION_QUERY
                    else:
                        description = ""

                    if block.target_endpoint == "https://sparql.swisslipids.org/sparql/":
                        description += SWISSLIPIDS_DESCRIPTION_QUERY
                    elif block.target_endpoint == "https://sparql.uniprot.org/sparql":
                        description += UNIPROT_DESCRIPTION_QUERY
                    elif block.target_endpoint == "https://sparql.rhea-db.org/sparql":
                        description += RHEA_DESCRIPTION_QUERY
                    else:
                        description += ""
                
                if block.endpoint != block.target_endpoint:
                    message = await prompt_template_service.ainvoke(
                        {
                            "input": state.messages[-1].content,
                            "extracted_example_queries": state.extracted_example_queries,
                            "service_endpoint": block.endpoint,
                            "target_endpoint": block.target_endpoint,
                            "iri_mapping": block.iri_map,
                            "endpoint_description": description,
                            "failed_pattern": block.failed_patterns if block.failed_patterns else "None"
                        }
                    )
                else:
                    message = await prompt_template_primary.ainvoke(
                        {
                            "input": state.messages[-1].content,
                            "extracted_example_queries": state.extracted_example_queries,
                            "target_endpoint": block.target_endpoint,
                            "iri_mapping": block.iri_map,
                            "endpoint_description": description,
                            "failed_pattern": block.failed_patterns if block.failed_patterns else "None"
                        }
                    )

                candidate: Candidate = await llm.ainvoke(message)

                syntax_validation = validate_sparql_syntax(candidate.pattern)

                if not syntax_validation[0]:
                    block.attempt += 1
                    block.failed_patterns.append({"pattern": candidate.pattern, "error_message": syntax_validation[1]})
                    continue
                else:
                    validation = query_sparql_wrapper(candidate.pattern, block.target_endpoint, timeout=120)
                    # Check for specific format: {'head': {'link': []}, 'boolean': False}
                    if validation is not None and isinstance(validation, dict) and validation.get('boolean', None) is True:
                        block.validated_pattern = candidate.pattern
                        block.final = True
                        break
                    elif validation is not None and isinstance(validation, dict) and validation.get('boolean', None) is False:
                        block.attempt += 1
                        error_msg = "Validation failed: Empty result or ASK query returned False"
                        block.failed_patterns.append({"pattern": candidate.pattern, "error_message": error_msg})
                        continue
                    else: 
                        block.attempt += 1
                        error_message = str(validation) if not isinstance(validation, str) else validation
                        block.failed_patterns.append({"pattern": candidate.pattern, "error_message": error_message})
                        continue

            
        return {
            "query_state": state.query_state,
            "steps": [
                StepOutput(
                    label="Pattern Generation",
                    details="Successfully generated patterns"
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in pattern generation",
                    details=f"Failed to generate pattern: {str(e)}",
                    type="fix-message"
                )
            ]
        }
                
        