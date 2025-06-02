#!/usr/bin/env python
import argparse
import asyncio
import os
import traceback
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
from experiments.utilities.evaluation import AgentEvaluator

async def main():
    endpoint_sets = { "SwissLipids": [], "Uniprot": [], "Rhea": [] }
    experiment_dir = os.path.join(project_root, "experiments/experiment_data")
    project_name = "your_project_name"
    timeout = 300
    tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
    dataset_dir = os.path.join(project_root, "experiments/federated_sparql_dataset/examples_federated_19.04.2025")
    
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
