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
import os
import pathlib
import logging

logger = logging.getLogger(__name__)

"""
This node is used for CP-A and LtM. It is used to retrieve relevant example queries to the user question from a vector database.
The settings and thresholds are defined in the configuration file.
"""

def format_retrieved_examples(examples_list):
    """Format the retrieved example queries for display in the agent UI.
    
    Args:
        examples_list: A list of Document objects with metadata containing example information
        
    Returns:
        A formatted markdown string for display in the UI
    """
    result = ""
    
    if not examples_list:
        return "No example queries found.\n\n"
    
    for i, doc in enumerate(examples_list):
        score = doc.metadata.get("score", 0)
        endpoint_url = doc.metadata.get("endpoint_url", "N/A")
        doc_type = doc.metadata.get("doc_type", "N/A")
        answer = doc.metadata.get("answer", "N/A")
        question = doc.metadata.get("question", "N/A")
        query_type = doc.metadata.get("query_type", "N/A")
        
        result += f"**Example Query {i+1}: {question}**\n\n"
        result += f"- [{score:.3f}] {doc.page_content}\n"
        result += f"  Endpoint URL: {endpoint_url}\n"
        result += f"  Doc Type: {doc_type}\n"
        result += f"  Query Type: {query_type}\n"
        result += f"  SPARQL Query (answer):\n\n```sparql\n{answer}\n```\n\n"
    
    return result




async def retrieve_examples(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """
    Retrieve example queries using dense vector search.
    
    Args:
        state: The current state 
        config: Configuration for the runnable
        
    Returns:
        Dictionary with example queries
    """

    matches = []
    steps = []

    configuration = Configuration.from_runnable_config(config)
    rag_config = configuration.rag_config
    cache_dir = rag_config.embeddings_cache_dir
    pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)
    try:
        dense_embeddings = FastEmbedEmbeddings(
            model_name=rag_config.dense_embedding_model_example_retrieval,
            cache_dir=cache_dir,
        )
        client = QdrantClient(
            host=rag_config.host,
            grpc_port=rag_config.grpc_port,
            prefer_grpc=True,
            timeout=rag_config.timeout
        )
        dense_vector = dense_embeddings.embed_query(state.messages[-1].content)

        if dense_vector is not None:
            logger.info(f"Querying Qdrant for example queries: {state.messages[-1].content}")
            results = client.query_points(
                collection_name=rag_config.collection_name_example_retrieval,
                query=dense_vector,
                using="dense",
                with_payload=True,
                limit=rag_config.top_k_example_retrieval,
            )

            for r_idx, point in enumerate(results.points):

                if point.score < rag_config.example_retrieval_threshold:
                    doc = Document(
                        page_content=point.payload.get("page_content", ""),
                        metadata={
                            **point.payload.get("metadata", {}),
                            "score": point.score 
                        }
                    )
                    matches.append(doc)
            logger.info(f"Found {len(matches)} matches for question: {state.messages[-1].content}")

        else:
            logger.warning(f"Empty embedding vector for question: {state.messages[-1].content}")
            matches = []

        steps.append(
            StepOutput(
                label=f"Retrieved {len(matches)} example queries",
                details=format_retrieved_examples(matches),
            )
        )
    
        return {
            "extracted_example_queries": matches,
            "steps": steps,
        }

    except Exception as e:
        error_message = f"Error in example resolution: {str(e)}"
        logger.error(error_message)
        import traceback
        logger.debug(traceback.format_exc())

        return {
            "extracted_example_queries": [],
            "steps": [
                StepOutput(
                    label="Example query retrieval failed",
                    details=f"Error: {error_message}\n\nPlease check that the embedding model and Qdrant server are accessible.",
                )
            ],
        }
        
        
