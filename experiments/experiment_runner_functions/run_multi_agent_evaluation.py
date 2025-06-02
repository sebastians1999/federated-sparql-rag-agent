import argparse
import asyncio
import os
import traceback
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
from experiments.utilities.multi_run_evaluator import MultiRunEvaluator

async def main():
    endpoint_sets = { "SwissLipids": [], "Uniprot": [], "Rhea": [] }
    experiment_dir = os.path.join(project_root, "experiments/experiment_data")
    project_name = "your_project_name"
    timeout = 600
    tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
    dataset_dir = os.path.join(project_root, "experiments/federated_sparql_dataset/examples_federated_19.04.2025")
    num_runs = 10
    evaluator = MultiRunEvaluator(
        num_runs=num_runs,
        endpoint_sets=endpoint_sets,
        experiment_dir=experiment_dir,
        project_name_langsmith=project_name,
        timeout=timeout,
        tracked_token_nodes=tracked_token_nodes,
        dataset_dir=dataset_dir
    )
    
    try:
        evaluation_results = await evaluator.run_experiments_async()
        print(f"\nMulti-run evaluation complete! Results saved to: {evaluator.run_dir}")
        return evaluation_results
    except Exception as e:
        print(f"Error during multi-run evaluation: {str(e)}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(main())
