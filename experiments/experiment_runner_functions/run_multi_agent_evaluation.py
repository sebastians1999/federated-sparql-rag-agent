import argparse
import asyncio
import os
import traceback
import sys
sys.path.append('/Users/sebastian/Documents/Bachelor Thesis/sparql-rag-agent/sparql-rag-agent')
from experiments.utilities.multi_run_evaluator import MultiRunEvaluator

async def main():
    """
    Run the multi-run agent evaluation with the exact configuration from the Jupyter notebook.
    """
    endpoint_sets = { "SwissLipids": [], "Uniprot": [], "Rhea": [] }
    experiment_dir = "experiments/experiment_data"
    project_name = "pattern_assembler_v1.0_gemini-2.5-flash-preview-05-20"
    timeout = 600
    tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
    dataset_dir = "/Users/sebastian/Documents/Bachelor Thesis/sparql-rag-agent/sparql-rag-agent/experiments/federated_sparql_dataset/examples_federated_19.04.2025"
    num_runs = 2
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
