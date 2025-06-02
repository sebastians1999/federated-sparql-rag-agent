from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, NamedVector, NamedSparseVector, SparseIndexParams, SparseVector
from langchain_qdrant.fastembed_sparse import FastEmbedSparse
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import gc
import time
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http import models
from sparql_llm import SparqlExamplesLoader, SparqlInfoLoader, SparqlVoidShapesLoader
from langchain_core.documents import Document
import argparse

"""
Indexes example SPARQL queries from specified endpoints into a Qdrant vector database.

This script connects to a Qdrant instance, (re)creates a collection, and embeds example SPARQL queries
from biomedical endpoints (UniProt, Rhea, SwissLipids by default) using a configurable embedding model.
The embedded queries are then indexed for efficient semantic search and retrieval.

Arguments:
    --host           Qdrant host (default: localhost)
    --port           Qdrant HTTP port (default: 6333)
    --grpc-port      Qdrant gRPC port (default: 6334)
    --collection     Name of the Qdrant collection (default: biomedical_examples_collection_v1.0)
    --model          Embedding model name (default: BAAI/bge-large-en-v1.5)
    --vector-size    Size of the embedding vectors (default: 384)
    --parallel       Number of parallel embedding threads (default: 4)

Modify the endpoints list in the script to index examples from other SPARQL endpoints as needed.
"""



def init_endpoint_examples(endpoints: List[str], collection_name: str = "biomedical_examples_collection_v1.0", embedding_model: str = "BAAI/bge-base-en-v1.5", parallel: int = 4, vector_size: int = 768, host: str = "localhost", port: int = 6333, grpc_port: int = 6334) -> None:

    client = QdrantClient(
            host=host,
            port=port,
            grpc_port=grpc_port,
            prefer_grpc=True,
            timeout=60
        )

    collections = client.get_collections()

    if collection_name in [c.name for c in collections.collections]:
        print(f"Collection '{collection_name}' exists, deleting...")
        client.delete_collection(collection_name)
    
    client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "dense": models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            },
            hnsw_config=models.HnswConfigDiff(
                on_disk=True
            ),
        )
    
    docs = []
 
    for endpoint in endpoints:
        docs += SparqlExamplesLoader(endpoint_url=endpoint).load()
    
    print(f"Loaded {len(docs)} documents from {len(endpoints)} endpoints")

    start_time = time.time()

    QdrantVectorStore.from_documents(
        docs,
        host=host,
        port=port,
        grpc_port=grpc_port,
        prefer_grpc=True,
        collection_name=collection_name,
        force_recreate=True,
        embedding=FastEmbedEmbeddings(model_name=embedding_model, parallel=parallel),
        vector_name="dense"
    )

    print(f"Done generating and indexing {len(docs)} documents into the vectordb in {time.time() - start_time} seconds")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Index SPARQL endpoint examples into Qdrant')
    parser.add_argument('--host', type=str, default='localhost', help='Qdrant host')
    parser.add_argument('--port', type=int, default=6333, help='Qdrant HTTP port')
    parser.add_argument('--grpc-port', type=int, default=6334, help='Qdrant gRPC port')
    parser.add_argument('--collection', type=str, default='biomedical_examples_collection_v1.0', help='Collection name')
    parser.add_argument('--model', type=str, default='BAAI/bge-large-en-v1.5', help='Embedding model name')
    parser.add_argument('--vector-size', type=int, default=384, help='Vector size')
    parser.add_argument('--parallel', type=int, default=4, help='Parallel processing threads')
    
    args = parser.parse_args()
    
    endpoints = [
        "https://sparql.uniprot.org/sparql/",
        "https://sparql.rhea-db.org/sparql/",
        "https://beta.sparql.swisslipids.org/",
    ]
    
    init_endpoint_examples(
        endpoints=endpoints,
        collection_name=args.collection,
        embedding_model=args.model,
        vector_size=args.vector_size,
        parallel=args.parallel,
        host=args.host,
        port=args.port,
        grpc_port=args.grpc_port
    )
