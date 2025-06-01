from langchain_core.runnables import RunnableConfig
from scr.agent.state.state import State, StepOutput
from typing import List, Dict
from scr.agent.utils.config import Configuration
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from scr.agent.prompts.LtM import QUERY_ASSEMBLE_PROMPT
from scr.agent.utils.llm_utils import get_llm
from typing import List, Dict, Optional
import re
import gc

# This node is part of the LtM methodology. It is used to assemble the final SPARQL query from the building blocks.


async def assemble_query(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:


    configuration = Configuration.from_runnable_config(config)


    try:

        llm = get_llm(configuration, task="sparql_construction", provider_key="provider_sparql_construction", model_key="sparql_construction_model")

        prompt_template = PromptTemplate(
            template=QUERY_ASSEMBLE_PROMPT,
            input_variables=["input", "federated_endpoints", "iri_mapping","building_blocks","target_endpoint", "extracted_example_queries"],
            template_format="jinja2"
        )


        building_blocks = ""
        for block in state.query_state.blocks:
            building_blocks += f"## Endpoint: {block.endpoint}\n\n"
            
            if block.final:
                building_blocks += "### Successful pattern:\n```\n"
                building_blocks += block.validated_pattern
                building_blocks += "\n```\n\n"
            else:
                building_blocks += "### Failed patterns:\n\n"
                
                # Group similar patterns to avoid repetition
                seen_patterns = {}
                for pattern in block.failed_patterns:
                    pattern_str = pattern.get("pattern", "")
                    error_msg = pattern.get("error_message", "")
                    
                    if pattern_str not in seen_patterns:
                        seen_patterns[pattern_str] = error_msg
                
                for pattern_str, error_msg in seen_patterns.items():
                    building_blocks += "```\n"
                    building_blocks += pattern_str
                    building_blocks += "\n```\n"
                    building_blocks += f"Error: {error_msg}\n\n"
                
            building_blocks += "\n"


        message = await prompt_template.ainvoke(
            {
                "input": state.messages[-1].content,
                # Exclude target endpoint from federated endpoints
                "federated_endpoints": [endpoint for endpoint in state.query_state.query_plan.federated_endpoints 
                                  if endpoint != state.query_state.query_plan.target_endpoint],
                "iri_mapping": state.query_state.query_plan.iri_map,
                "building_blocks": building_blocks,
                "target_endpoint": state.query_state.query_plan.target_endpoint,
                "extracted_example_queries": state.extracted_example_queries
            }
        )

        response_message = await llm.ainvoke(message)

        extracted_queries = extract_sparql_queries(response_message.content)

        gc.collect()

        return {
            "structured_output": extracted_queries[-1] if extracted_queries else "",
            "steps": [
                StepOutput(
                    label="Assembled SPARQL query",
                    details=response_message.content,
                )
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "steps": [
                StepOutput(
                    label="Error in SPARQL query assembly",
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
