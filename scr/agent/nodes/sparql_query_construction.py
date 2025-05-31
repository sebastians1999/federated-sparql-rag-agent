from scr.agent.state.state import State, StepOutput
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Optional
from scr.agent.utils.config import Configuration
from langchain_core.runnables import RunnableConfig
from scr.agent.utils.llm_utils import get_llm
import re
from  scr.agent.prompts.few_shot_CoT import examples_few_shot_federated_query_generation
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate

from scr.agent.prompts.CP import CONSTRUCTION_PROMPT
from scr.agent.prompts.CP_A import CONSTRUCTION_PROMPT_AUGMENTED
from scr.agent.prompts.general import INTRODUCTION_PROMPT, ENPOINT_INFORMATION_PROMPT, QUERY_FORMAT_PROMPT
from scr.agent.prompts.Baseline import BASELINE_PROMPT


# This file contains two nodes: 
# 1. query_generator: Generates a SPARQL. This function was modified slightly, depending on the methodology used (baseline, CP, CP-A, CoT).
#   - CP: Outcomment the part where no retrieved examples are provided. 
#   - CP-A: Currently set.
#   - CoT: Use CP and for ("human","{{input}}") put "USER_PROMPT".


# 2. query_generator_few_shot_cot: Generates a SPARQL query based on the structured question and retrieved documents using few-shot COT.


async def query_generator_baseline(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """                 
    
    try:                             

        configuration = Configuration.from_runnable_config(config)


        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = ChatPromptTemplate(
            [
                ("system", BASELINE_PROMPT),
                ("human", "{{input}}")
            ],
            input_variables=["input", "potential_entities", "potential_classes", "extracted_example_queries"],
            template_format="jinja2"
        )


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
                "extracted_example_queries": state.extracted_example_queries
            }
        )
        
        response_message = await llm.ainvoke(message)


        extracted_queries = extract_sparql_queries(response_message.content)
    

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Generated SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query generation",
                    details=f"Failed to generate query: {str(e)}",
                    type="fix-message"
                )
            ]
        }



async def query_generator_cp(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """                 
    
    try:                             

        configuration = Configuration.from_runnable_config(config)


        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = ChatPromptTemplate(
            [
                ("system", CONSTRUCTION_PROMPT),
                ("human", "{{input}}")
            ],
            input_variables=["input", "potential_entities", "potential_classes", "extracted_example_queries"],
            template_format="jinja2"
        )


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
                "extracted_example_queries": state.extracted_example_queries
            }
        )
        
        response_message = await llm.ainvoke(message)


        extracted_queries = extract_sparql_queries(response_message.content)
    

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Generated SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query generation",
                    details=f"Failed to generate query: {str(e)}",
                    type="fix-message"
                )
            ]
        }

async def query_generator_cp_augmented(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """                 
    
    try:                             

        configuration = Configuration.from_runnable_config(config)

        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = ChatPromptTemplate(
            [
                ("system", CONSTRUCTION_PROMPT_AUGMENTED),
                ("human", "{{input}}")
            ],
            input_variables=["input", "potential_entities", "potential_classes", "extracted_example_queries"],
            template_format="jinja2"
        )


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
                "extracted_example_queries": state.extracted_example_queries
            }
        )
        
        response_message = await llm.ainvoke(message)


        extracted_queries = extract_sparql_queries(response_message.content)
    

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Generated SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query generation",
                    details=f"Failed to generate query: {str(e)}",
                    type="fix-message"
                )
            ]
        }

async def query_generator_cot(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """                 
    
    try:                             

        configuration = Configuration.from_runnable_config(config)

        USER_PROMPT = """{{input}}\n\nThink step by step.""" 


        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = ChatPromptTemplate(
            [
                ("system", CONSTRUCTION_PROMPT),
                ("human", USER_PROMPT)
            ],
            input_variables=["input", "potential_entities", "potential_classes", "extracted_example_queries"],
            template_format="jinja2"
        )


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
                "extracted_example_queries": state.extracted_example_queries
            }
        )
        
        response_message = await llm.ainvoke(message)


        extracted_queries = extract_sparql_queries(response_message.content)
    

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Generated SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query generation",
                    details=f"Failed to generate query: {str(e)}",
                    type="fix-message"
                )
            ]
        }



async def query_generator_few_shot_cot(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """
    
    try:

        configuration = Configuration.from_runnable_config(config)

     


        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        context_template = PromptTemplate(
            template_format='jinja2',
            input_variables=["potential_entities", "potential_classes"],
            template= QUERY_FORMAT_PROMPT
        )

        formatted_context= await context_template.ainvoke({
            "potential_entities": state.extracted_entities, 
            "potential_classes": state.extracted_classes
        })

        example_template = PromptTemplate(
            template_format='jinja2',
            input_variables=["Input", "Context", "Endpoint_information", "Assistant"],
            template="**User:**\n{{ Input }}\n\n**Context:**\n{{ Context }}\n\n**Endpoint Information:**\n{{ Endpoint_information }}\n\n**Assistant:**\n{{ Assistant }}\n\n"
        )

        few_shot_prompt = FewShotPromptTemplate(
            examples=examples_few_shot_federated_query_generation,
            example_prompt=example_template,
            input_variables=["Input", "Context", "Endpoint_information"],
            prefix=INTRODUCTION_PROMPT,
            suffix="**User:**\n{{ Input }}\n\n**Context:**\n{{ Context }}\n\n**Endpoint Information:**\n{{ Endpoint_information }}\n\n**Assistant:**",
            template_format="jinja2" 
        )


        message = await few_shot_prompt.ainvoke({
            "Input": state.messages[-1].content,
            "Context": formatted_context.to_string(),
            "Endpoint_information": ENPOINT_INFORMATION_PROMPT,
        })

        #print(formatted_context.to_string())

        #print(message.to_string())

        response_message = await llm.ainvoke(message)


        extracted_queries = extract_sparql_queries(response_message.content)
    

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Generated SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query generation",
                    details=f"Failed to generate query: {str(e)}",
                    type="fix-message"
                )
            ]
        }



queries_pattern = re.compile(r"```sparql(.*?)```", re.DOTALL)
endpoint_pattern = re.compile(r"^#.*(https?://[^\s]+)", re.MULTILINE)


def extract_sparql_queries(md_resp: str) -> list[dict[str, Optional[str]]]:
    """Extract SPARQL queries and endpoint URL from a markdown response."""
    extracted_queries = []
    queries = queries_pattern.findall(md_resp)
    for query in queries:
        extracted_endpoint = endpoint_pattern.search(query.strip())
        if extracted_endpoint:
            extracted_queries.append(
                {
                    "query": str(query).strip(),
                    "endpoint_url": str(extracted_endpoint.group(1)) if extracted_endpoint else None,
                }
            )
    return extracted_queries
