import os
import json
import numpy as np
import scipy.stats
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from .evaluation import AgentEvaluator

class MultiRunEvaluator:
    """
    Runs multiple instances of AgentEvaluator and calculates aggregate statistics
    with confidence intervals across all runs.
    """
    
    def __init__(
        self, 
        num_runs: int = 10,
        endpoint_sets: Dict = None,
        experiment_dir: str = "experiments_official_sample_runs",
        project_name_langsmith: str = None,
        timeout: int = 300,
        tracked_token_nodes: List[str] = ["question_understanding", "sparql_query_construction"],
        dataset_dir: str = None
    ):
        """
        Initialize the MultiRunEvaluator.
        
        Args:
            num_runs: Number of evaluation runs to perform
            endpoint_sets: Dictionary mapping endpoint names to their files
            experiment_dir: Parent directory to store all experiment runs
            project_name_langsmith: Base name for the LangSmith project
            timeout: Timeout in seconds for each query execution
            tracked_token_nodes: List of node names to track token usage for
            dataset_dir: Directory containing the dataset files
        """
        self.num_runs = num_runs
        self.endpoint_sets = endpoint_sets
        # Always prepend 'experiments/' to the experiment_dir to ensure it works from project root
        self.experiment_dir = os.path.join("experiments", experiment_dir)
        self.project_name_langsmith = project_name_langsmith
        self.timeout = timeout
        self.tracked_token_nodes = tracked_token_nodes
        self.dataset_dir = dataset_dir
        self.results = []
        
        # Create the parent directory if it doesn't exist
        os.makedirs(self.experiment_dir, exist_ok=True)
        
        # Timestamp for this multi-run evaluation
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.run_dir = os.path.join(self.experiment_dir, f"multi_run_{self.timestamp}")
        os.makedirs(self.run_dir, exist_ok=True)
    
    def run_experiments(self) -> Dict[str, Any]:
        """
        Run multiple experiments and collect their results.
        
        Returns:
            Dictionary containing aggregate statistics
        """
        # Get the current event loop or create a new one
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an event loop (e.g., in a Jupyter notebook)
                # In this case it's better to directly use 'await evaluator.run_experiments_async()' 
                # in your notebook instead of this method
                return asyncio.get_event_loop().run_until_complete(self.run_experiments_async())
            else:
                # No running event loop, use run_until_complete
                return loop.run_until_complete(self.run_experiments_async())
        except RuntimeError:
            # No event loop exists yet, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self.run_experiments_async())
            finally:
                loop.close()
        
    async def run_experiments_async(self) -> Dict[str, Any]:
        """
        Async implementation to run multiple experiments and collect their results.
        
        Returns:
            Dictionary containing aggregate statistics
        """
        print(f"Starting {self.num_runs} evaluation runs...")
        
        for i in range(self.num_runs):
            print(f"Running experiment {i+1}/{self.num_runs}")
            
            # Create a unique subdirectory for this run
            run_subdir = f"run_{i+1}"
            full_run_dir = os.path.join(self.run_dir, run_subdir)
            
            # Initialize and run evaluator
            evaluator = AgentEvaluator(
                endpoint_sets=self.endpoint_sets,
                experiment_dir=full_run_dir,
                project_name_langsmith=self.project_name_langsmith,
                timeout=self.timeout,
                tracked_token_nodes=self.tracked_token_nodes,
                dataset_dir=self.dataset_dir
            )
            
            # Run the evaluation - this saves results in the specified directory
            await evaluator.run_all_tests()
            
            # Retrieve the metrics from the saved file
            metrics_file = os.path.join("experiments", full_run_dir, 'metrics_dataset.json')
            try:
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
                    self.results.append(metrics)
                    print(f"Run {i+1} completed successfully")
            except Exception as e:
                print(f"Error reading metrics from run {i+1}: {str(e)}")
        
        # Calculate and save statistics
        statistics = self.calculate_statistics()
        return statistics
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Calculate aggregate statistics across all runs.
        
        Returns:
            Dictionary containing statistics with means and confidence intervals
        """
        if not self.results:
            print("No results to analyze. Please run experiments first.")
            return {}
        
        # Key metrics to analyze
        key_metrics = [
            "avg_result_excluding_empty_result_precision",
            "avg_result_excluding_empty_result_recall",
            "avg_result_excluding_empty_result_f1",
            "avg_result_including_empty_result_precision",
            "avg_result_including_empty_result_recall",
            "avg_result_including_empty_result_f1",
            "avg_result_all_precision",
            "avg_result_all_recall",
            "avg_result_all_f1"
        ]
        
        # Extract values for each metric across all runs
        metric_values = {metric: [] for metric in key_metrics}
        for result in self.results:
            for metric in key_metrics:
                if metric in result:
                    metric_values[metric].append(result[metric])
        
        # Calculate mean and confidence interval for each metric
        statistics = {}
        for metric, values in metric_values.items():
            if not values:
                continue
                
            values_array = np.array(values, dtype=float)
            mean = np.mean(values_array)
            

            # Calculate confidence interval with unknown population standard deviation/variance
            if len(values) > 1:
                sem = scipy.stats.sem(values_array)
                ci = scipy.stats.t.interval(0.95, len(values_array)-1, loc=mean, scale=sem)
                ci_lower, ci_upper = ci
            else:
                ci_lower, ci_upper = mean, mean
                
            statistics[metric] = {
                "mean": float(mean),
                "ci_lower": float(ci_lower),
                "ci_upper": float(ci_upper),
                "std_dev": float(np.std(values_array)),
                "values": values,
                "n": len(values)
            }
        
        # Save aggregate statistics
        stats_file = os.path.join("experiments", self.run_dir, f"aggregate_statistics.json")
        with open(stats_file, "w") as f:
            json.dump(statistics, f, indent=2)
            
        # Also save the raw results from all runs
        all_runs_file = os.path.join("experiments", self.run_dir, f"all_runs_data.json")
        with open(all_runs_file, "w") as f:
            json.dump(self.results, f, indent=2)
            
        return statistics

    def summarize_results(self) -> Dict[str, Any]:
        """
        Print a summary of the results with means and confidence intervals.
        
        Returns:
            Dictionary containing statistics
        """
        stats = self.calculate_statistics()
        if not stats:
            return {}
            
        print(f"\n===== Summary of {self.num_runs} Experiment Runs =====\n")
        
        print("Metric Categories:")
        categories = [
            ("Excluding Empty Results", ["avg_result_excluding_empty_result_precision", 
                                         "avg_result_excluding_empty_result_recall", 
                                         "avg_result_excluding_empty_result_f1"]),
            ("Including Empty Results", ["avg_result_including_empty_result_precision",
                                         "avg_result_including_empty_result_recall",
                                         "avg_result_including_empty_result_f1"]),
            ("All Results", ["avg_result_all_precision", 
                             "avg_result_all_recall", 
                             "avg_result_all_f1"])
        ]
        
        for category_name, metrics in categories:
            print(f"\n{category_name}:")
            for metric in metrics:
                if metric in stats:
                    mean = stats[metric]["mean"]
                    ci_lower = stats[metric]["ci_lower"]
                    ci_upper = stats[metric]["ci_upper"]
                    n = stats[metric]["n"]
                    std_dev = stats[metric]["std_dev"]
                    
                    metric_display = metric.replace("avg_result_", "").replace("_", " ").title()
                    print(f"  {metric_display}: {mean:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}], n={n}, std={std_dev:.4f})")
        
        print(f"\nDetailed statistics saved to: {os.path.join('experiments', self.run_dir)}/aggregate_statistics.json")
        
        return stats

def calculate_statistics_for_existing_runs(multi_run_path: str) -> Dict[str, Any]:
    """
    Calculate statistics for an existing multi-run experiment.
    
    This function can be used to generate statistics for a previous multi-run experiment
    that may have failed to calculate statistics when it was first run.
    
    Args:
        multi_run_path: Path to the multi-run directory (e.g., 'experiments/experiments_official/multi_run_2025-05-02_00-31-21')
        
    Returns:
        Dictionary containing statistics with means and confidence intervals
    """
    print(f"Calculating statistics for: {multi_run_path}")
    
    # Find all run directories
    results = []
    
    # List all directories in the multi_run_path to find run_X directories
    try:
        run_dirs = [d for d in os.listdir(multi_run_path) if d.startswith("run_") and os.path.isdir(os.path.join(multi_run_path, d))]
        run_dirs.sort(key=lambda x: int(x.split("_")[1]))  # Sort by run number
        
        if not run_dirs:
            print(f"No run directories found in {multi_run_path}")
            return {}
            
        print(f"Found {len(run_dirs)} run directories")
        
        for run_dir in run_dirs:
            run_number = int(run_dir.split("_")[1])
            full_run_path = os.path.join(multi_run_path, run_dir)
            
            # Check if there's an evaluation directory (ev_*) inside the run directory
            try:
                ev_dirs = [d for d in os.listdir(full_run_path) if d.startswith("ev_") and os.path.isdir(os.path.join(full_run_path, d))]
                
                if ev_dirs:
                    # Use the first evaluation directory found
                    ev_dir = ev_dirs[0]
                    metrics_file = os.path.join(full_run_path, ev_dir, 'metrics_dataset.json')
                    
                    if os.path.exists(metrics_file):
                        try:
                            with open(metrics_file, 'r') as f:
                                metrics = json.load(f)
                                results.append(metrics)
                                print(f"Loaded metrics from run {run_number} (evaluation dir: {ev_dir})")
                        except Exception as e:
                            print(f"Error reading metrics from run {run_number}: {str(e)}")
                    else:
                        print(f"No metrics file found in {metrics_file}")
                else:
                    # Try the direct path (old structure)
                    metrics_file = os.path.join(full_run_path, 'metrics_dataset.json')
                    if os.path.exists(metrics_file):
                        try:
                            with open(metrics_file, 'r') as f:
                                metrics = json.load(f)
                                results.append(metrics)
                                print(f"Loaded metrics from run {run_number} (direct path)")
                        except Exception as e:
                            print(f"Error reading metrics from run {run_number}: {str(e)}")
                    else:
                        print(f"No metrics file found in run directory: {full_run_path}")
            except Exception as e:
                print(f"Error listing evaluation directories in {full_run_path}: {str(e)}")
                
    except Exception as e:
        print(f"Error listing directories in {multi_run_path}: {str(e)}")
        return {}
    
    print(f"Successfully processed {len(results)} runs")
    
    if not results:
        print("No results to analyze.")
        return {}
    
    # Key metrics to analyze
    key_metrics = [
        "avg_result_excluding_empty_result_precision",
        "avg_result_excluding_empty_result_recall",
        "avg_result_excluding_empty_result_f1",
        "avg_result_including_empty_result_precision",
        "avg_result_including_empty_result_recall",
        "avg_result_including_empty_result_f1",
        "avg_result_all_precision",
        "avg_result_all_recall",
        "avg_result_all_f1"
    ]
    
    # Extract values for each metric across all runs
    metric_values = {metric: [] for metric in key_metrics}
    for result in results:
        for metric in key_metrics:
            if metric in result:
                metric_values[metric].append(result[metric])
    
    # Calculate mean and confidence interval for each metric
    statistics = {}
    for metric, values in metric_values.items():
        if not values:
            continue
            
        values_array = np.array(values, dtype=float)
        mean = np.mean(values_array)
        
        # Calculate confidence interval with unknown population standard deviation/variance
        if len(values) > 1:
            sem = scipy.stats.sem(values_array)
            ci = scipy.stats.t.interval(0.95, len(values_array)-1, loc=mean, scale=sem)
            ci_lower, ci_upper = ci
        else:
            ci_lower, ci_upper = mean, mean
            
        statistics[metric] = {
            "mean": float(mean),
            "ci_lower": float(ci_lower),
            "ci_upper": float(ci_upper),
            "std_dev": float(np.std(values_array)),
            "values": values,
            "n": len(values)
        }
    
    # Save aggregate statistics
    stats_file = os.path.join(multi_run_path, "aggregate_statistics.json")
    with open(stats_file, "w") as f:
        json.dump(statistics, f, indent=2)
        
    # Also save the raw results from all runs
    all_runs_file = os.path.join(multi_run_path, "all_runs_data.json")
    with open(all_runs_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print a summary of the results
    print("\nStatistics Summary:")
    for metric, stats in statistics.items():
        mean = stats["mean"]
        ci_lower = stats["ci_lower"]
        ci_upper = stats["ci_upper"]
        std_dev = stats["std_dev"]
        n = stats["n"]
        metric_display = metric.replace("avg_result_", "").replace("_", " ").title()
        print(f"  {metric_display}: {mean:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}], n={n}, std={std_dev:.4f})")
    
    print(f"\nDetailed statistics saved to: {stats_file}")
    
    return statistics
