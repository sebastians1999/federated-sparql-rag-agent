#!/usr/bin/env python3
import argparse
import ray
import time
from endpoint_loader import load_entities_from_endpoints
from entities_collection import entities_list
from entity_indexing_pipeline_v3 import EmbeddingPipeline


def main():
    parser = argparse.ArgumentParser(description='Load and embed biomedical entities into Qdrant')
    parser.add_argument('--host', type=str, default='localhost', help='Qdrant host')
    parser.add_argument('--grpc-port', type=int, default=6334, help='Qdrant gRPC port')
    parser.add_argument('--collection', type=str, default='test_collection', help='Collection name')
    parser.add_argument('--dense-model', type=str, default='BAAI/bge-small-en-v1.5', help='Dense embedding model name')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--batch-size', type=int, default=144, help='Batch size for indexing')
    parser.add_argument('--recreate',type=bool, default=False, help='Recreate collection if it exists')
    parser.add_argument('--log-dir', type=str, default='./upload_logs', help='Directory for upload logs')
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    ray.init(ignore_reinit_error=True)
    
    try:
        print("Loading entities from SPARQL endpoints...")
        entities = load_entities_from_endpoints(entities_list)
        
    
        pipeline = EmbeddingPipeline(
            collection_name=args.collection,
            dense_model_name=args.dense_model,
            host=args.host,
            grpc_port=args.grpc_port,
            num_workers=args.workers,
            log_dir=args.log_dir,
            recreate_collection=args.recreate
        )
        
        pipeline.add_documents(entities, batch_size=args.batch_size)
        
        elapsed_time = (time.time() - start_time) / 60
        print(f"Total processing time: {elapsed_time:.2f} minutes")
        
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
