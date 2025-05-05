#!/usr/bin/env python
import argparse
import asyncio
import os
import traceback
import sys
sys.path.append('/Users/sebastian/Documents/Bachelor Thesis/sparql-rag-agent/sparql-rag-agent')
from experiments.utilities.evaluation import AgentEvaluator

async def main():
    """
    Run the agent evaluation with the exact configuration from the Jupyter notebook.
    """
    endpoint_sets = { "SwissLipids": [], "Uniprot": [], "Rhea": [] }
    experiment_dir = "experiments_official"
    project_name = "pattern_assembler_v1.0_gemini-2.0-flash"
    timeout = 300
    tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
    dataset_dir = "/Users/sebastian/Documents/Bachelor Thesis/sparql-rag-agent/sparql-rag-agent/experiments/federated_sparql_dataset/examples_federated_19.04.2025"
    
    evaluator = AgentEvaluator(
        endpoint_sets=endpoint_sets,
        experiment_dir=experiment_dir,
        project_name_langsmith=project_name,
        timeout=timeout,
        tracked_token_nodes=tracked_token_nodes,
        dataset_dir=dataset_dir
    )
    
    try:
        evaluation_dataset_path = await evaluator.run_all_tests()
        print(f"\nEvaluation complete! Results saved to: {evaluation_dataset_path}")
        return evaluation_dataset_path
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(main())
