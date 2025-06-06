from typing import Annotated, Sequence, TypedDict, Callable, Dict, Any, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from scr.agent.nodes.question_understanding import question_understanding
from scr.agent.nodes.entity_resolution import retrieve_entities_classes
from scr.agent.nodes.example_resolution import retrieve_examples
from scr.agent.nodes.planning import plan_query
from scr.agent.nodes.pattern import generate_and_validate_blocks
from scr.agent.nodes.sparql_query_construction import query_generator_few_shot_cot, query_generator_cp, query_generator_cp_augmented, query_generator_cot, query_generator_baseline
from scr.agent.state.state import State
from scr.agent.utils.config import Configuration
from scr.agent.nodes.assembler import assemble_query



def create_graph(config: Optional[Configuration] = None) -> Graph:
    """Create the agent workflow graph.
    
    Args:
        config: Configuration for the runner. If None, a default config will be created.
        
    Returns:
        The compiled graph
    """
    # Create default config if none provided
    if config is None:
        config = Configuration(test_mode=True)
    
    # Create a new graph
    workflow = StateGraph(State) 




    # Depending on which methodology you would like to use, please uncomment the corresponding section.
    # LtM is the default method.




    ############### Baseline ##############################

    # workflow.add_node("question_understanding", question_understanding)
    # workflow.add_node("entity_resolution", retrieve_entities_classes)
    # workflow.add_node("sparql_query_construction", query_generator_baseline)


    # workflow.add_edge("question_understanding", "entity_resolution")
    # workflow.add_edge("entity_resolution", "sparql_query_construction")

    # workflow.set_entry_point("question_understanding")
    # workflow.set_finish_point("sparql_query_construction")

    #########################################################


    ############### Construction Prompt (CP) ###############

    # workflow.add_node("question_understanding", question_understanding)
    # workflow.add_node("entity_resolution", retrieve_entities_classes)
    # workflow.add_node("sparql_query_construction", query_generator_cp)

    # workflow.add_edge("question_understanding", "entity_resolution")
    # workflow.add_edge("entity_resolution", "sparql_query_construction")

    # workflow.set_entry_point("question_understanding")
    # workflow.set_finish_point("sparql_query_construction")

    #########################################################


    ############## CoT ######################################

    # workflow.add_node("question_understanding", question_understanding)
    # workflow.add_node("entity_resolution", retrieve_entities_classes)
    # workflow.add_node("sparql_query_construction", query_generator_cot)


    # workflow.add_edge("question_understanding", "entity_resolution")
    # workflow.add_edge("entity_resolution", "sparql_query_construction")


    # workflow.set_entry_point("question_understanding")
    # workflow.set_finish_point("sparql_query_construction")

    ###########################################################


    ############### few-shot CoT ############################

    # workflow.add_node("question_understanding", question_understanding)
    # workflow.add_node("entity_resolution", retrieve_entities_classes)
    # workflow.add_node("sparql_query_construction", query_generator_few_shot_cot)


    # workflow.add_edge("question_understanding", "entity_resolution")
    # workflow.add_edge("entity_resolution", "sparql_query_construction")


    # workflow.set_entry_point("question_understanding")
    # workflow.set_finish_point("sparql_query_construction")

    ###########################################################


    ############### Augmented Construction Prompt (CP-A) ######

    # workflow.add_node("question_understanding", question_understanding)
    # workflow.add_node("entity_resolution", retrieve_entities_classes)
    # workflow.add_node("example_resolution", retrieve_examples)
    # workflow.add_node("sparql_query_construction", query_generator_cp_augmented)


    # workflow.add_edge("question_understanding", "entity_resolution")
    # workflow.add_edge("entity_resolution", "example_resolution")
    # workflow.add_edge("example_resolution", "sparql_query_construction")


    # workflow.set_entry_point("question_understanding")
    # workflow.set_finish_point("sparql_query_construction")

    ############################################################


    ############### Least-to-Most (LtM) ########################

    workflow.add_node("question_understanding", question_understanding)
    workflow.add_node("entity_resolution", retrieve_entities_classes)
    workflow.add_node("example_resolution", retrieve_examples)
    workflow.add_node("planning", plan_query)
    workflow.add_node("pattern", generate_and_validate_blocks)
    workflow.add_node("assembler", assemble_query)

    workflow.add_edge("question_understanding", "entity_resolution")
    workflow.add_edge("entity_resolution", "example_resolution")
    workflow.add_edge("example_resolution", "planning")
    workflow.add_edge("planning", "pattern")
    workflow.add_edge("pattern", "assembler")
    
    workflow.set_entry_point("question_understanding")
    workflow.set_finish_point("assembler")

    ############################################################


    # Compile the graph
    graph = workflow.compile()

    # Add config to graph
    graph.config_meta = config

    return graph 