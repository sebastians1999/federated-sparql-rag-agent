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
from langchain_core.prompts import ChatPromptTemplate
import os
import pathlib
import logging
from scr.agent.state.state import QueryPlan, QueryState, BlockState
from scr.agent.utils.llm_utils import get_llm
from scr.agent.prompts.prompts import QUERY_PLANNING_PROMPT

logger = logging.getLogger(__name__)


# This node is part of the LtM methodology. It is used to plan the query (entity mapping, initial SELECT variables, federated endpoints, target endpoint)

async def plan_query(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    
        
    configuration = Configuration.from_runnable_config(config)
    rag_config = configuration.rag_config

    if not state.messages:
        raise ValueError("No messages found in state")
    try:
        

        configuration = Configuration.from_runnable_config(config)

        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model").with_structured_output(schema = QueryPlan)


        prompt_template = ChatPromptTemplate(
             [
                ("system", QUERY_PLANNING_PROMPT),
                ("human", "{{input}}")
            ],
            template_format="jinja2",
            input_variables=["input", "entities_question", "classes_question", "potential_entities", "potential_classes", "extracted_example_queries"],
        )

        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "entities_question": state.structured_question.extracted_entities,
                "classes_question": state.structured_question.extracted_classes,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
                "extracted_example_queries": state.extracted_example_queries
            }
        )

        query_plan: QueryPlan = await llm.ainvoke(message)

        block_states = []
        for endpoint in query_plan.federated_endpoints:
            block_states.append(BlockState(endpoint=endpoint, iri_map=query_plan.iri_map, target_endpoint=query_plan.target_endpoint))

        query_state = QueryState(
            blocks=block_states,
            query_plan=query_plan,
            question=state.messages[-1].content
        )

        return {
            "query_state": query_state,
            "steps": [
                StepOutput(
                    label="Query Planning",
                    details="Successfully planned query"
                )
            ]
        }

    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in planning",
                    details=f"Failed to process question: {str(e)}",
                    type="fix-message"
                )
            ]
        }




    

