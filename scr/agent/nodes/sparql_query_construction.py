from scr.agent.state.state import State, StepOutput
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from scr.agent.prompts.prompts import QUERY_GENERATION_PROMPT
from typing import List, Dict, Optional
from scr.agent.utils.config import Configuration
from langchain_core.runnables import RunnableConfig
from scr.agent.utils.llm_utils import get_llm
import re
from  scr.agent.prompts.few_shot_examples import examples_few_shot_federated_query_generation
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from scr.agent.prompts.prompts import INTRODUCTION_PROMPT, ENPOINT_INFORMATION_PROMPT, QUERY_FORMAT_PROMPT, INTRODUCTION_PROMPT





async def query_generator(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generate a SPARQL query based on the structured question and retrieved documents.
    
    Args:
        state: The current state containing structured question and retrieved documents
        config: Configuration for the runner
        
    Returns:
        Dict containing structured_output and steps
    """
    
    try:

        configuration = Configuration.from_runnable_config(config)

        USER_PROMPT = "{input}\n\nThink step by step." 


        # Use per-task LLM config for SPARQL construction
        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", QUERY_GENERATION_PROMPT),
                ("human", "{input}")
            ]
        )
        #retrieved_documents
        #("human", "{input}")


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                "potential_entities": state.extracted_entities,
                "potential_classes": state.extracted_classes,
            }
        )
        #"retrieved_documents": [doc.page_content for doc in state.retrieved_docs],
        
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
            template="**User:**\n {{ Input }}\n\n**Context:**\n Potential {{ Context }}\n\n**Endpoint Information:**\n {{ Endpoint_information }}\n\n**Assistant:**\n {{ Assistant }}\n\n"
        )


        few_shot_prompt = FewShotPromptTemplate(
            examples=examples_few_shot_federated_query_generation,
            example_prompt=example_template,
            input_variables=["Input", "Context", "Endpoint_information"],
            prefix=INTRODUCTION_PROMPT,
            suffix="User: {{ Input }}\n\nContext: {{ Context }}\n\nEndpoint Information: {{ Endpoint_information }}\n\nAssistant:",
            template_format="jinja2" 
        )


        message = await few_shot_prompt.ainvoke({
            "Input": state.messages[-1].content,
            "Context": formatted_context,
            "Endpoint_information": ENPOINT_INFORMATION_PROMPT,
        })


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