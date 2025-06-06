import asyncio
import sys
import os
import time
from datetime import datetime
import dotenv
from scipy.special import elliprf
from experiments.utilities.format import process_federated_dataset, load_data_from_file, process_specific_datasets_and_files, save_queries_comparison
from datasets import Dataset
from scr.agent.state.state import State
from langchain_core.messages import HumanMessage
from scr.agent.utils.graph import create_graph
from langsmith import Client
from datasets import Dataset
from experiments.utilities.metrics import eval_pairs
import json
from experiments.utilities.sparql_syntax_validation import validate_sparql_syntax
from experiments.utilities.format import extract_endpoint_from_comment_regex
from experiments.utilities.result_metric import format_query_result_dataframe, calculate_column_metrics_with_label_similarity
from experiments.utilities.format import normalize_url
from experiments.utilities.experiment_metadata_writer import write_experiment_metadata
import traceback


class AgentEvaluator:

    """
    SPARQL RAG Agent Evaluation Framework

    This module provides the evaluation framework for evaluating the performance of the SPARQL query generation agent.
    It compares generated SPARQL queries against ground truth queries and calculates various metrics.


    Key Features:
    - Executes agent on natural language questions from evaluation dataset.
    - Validates generated SPARQL syntax.
    - Compares query results against ground truth.
    - Calculates precision, recall, and F1 scores for aligned query results.
    - Calculates translation metrics - SP-BLEU, METEOR - for SPARQL queries.
    - Tracks token usage and execution times.
    - Generates detailed evaluation reports.
    """
    
    def __init__(self, dataset_dir=None, output_dir=None, endpoint_sets=None, project_name_langsmith: str ="sparql-rag-agent", test: bool = False, experiment_dir: str = None, timeout: int = 300, tracked_token_nodes=None):
        
        self.endpoint_sets = endpoint_sets
        self.experiment_dir = experiment_dir
        self.dataset_dir = dataset_dir
        self.output_dir = process_specific_datasets_and_files(dataset_dir=self.dataset_dir, endpoint_files_map=self.endpoint_sets, output_dir=self.experiment_dir)
        self.test_dataset_path = os.path.join(self.output_dir, 'testset_meta_data.json')
        self.test_dataset = Dataset.from_dict(load_data_from_file(self.test_dataset_path))
        self.graph = create_graph()
        self.client = Client()
        self.project_name_langsmith = project_name_langsmith
        self.results = []
        self.evaluation_dataset_path = os.path.join(self.output_dir, 'evaluation_dataset.json')
        self.metric_dataset_path = os.path.join(self.output_dir, 'metrics_dataset.json')
        self.test = test
        self.timeout = timeout # timeout after 300 seconds
        self.tracked_token_nodes = tracked_token_nodes
        
        write_experiment_metadata(
            output_dir=self.output_dir,
            graph_config=getattr(self.graph, 'config_meta', None),
            #EXTRACTION_PROMPT,
            #QUERY_GENERATION_PROMPT,
            timeout=self.timeout
        )
        
    def read_dataset(self, dataset_path: str) -> Dataset:
        """Read the dataset from the given path."""
        result = load_data_from_file(dataset_path)
        return result
    
    def set_avg_metrics(self, results_dict, metric_prefix, total_precision, total_recall, total_f1, count, queries_list=None):
        """Calculate and set average metrics based on counts and totals."""
        if count > 0:
            results_dict[f"avg_result_{metric_prefix}_precision"] = total_precision / count
            results_dict[f"avg_result_{metric_prefix}_recall"] = total_recall / count
            results_dict[f"avg_result_{metric_prefix}_f1"] = total_f1 / count
            results_dict[f"number_of_query_results_evaluated_{metric_prefix}"] = count
            if queries_list is not None:
                results_dict[f"list_evaluated_queries_{metric_prefix}"] = queries_list
        else:
            results_dict[f"avg_result_{metric_prefix}_precision"] = 0.0
            results_dict[f"avg_result_{metric_prefix}_recall"] = 0.0
            results_dict[f"avg_result_{metric_prefix}_f1"] = 0.0
            results_dict[f"number_of_query_results_evaluated_{metric_prefix}"] = 0
            if queries_list is not None:
                results_dict[f"list_evaluated_queries_{metric_prefix}"] = []

    def ensure_serializable(self, obj):
        """Ensure all items in a data structure are JSON-serializable.
        
        Recursively processes nested structures and converts non-serializable objects to strings.
        """
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self.ensure_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.ensure_serializable(v) for k, v in obj.items()}
        else:
            return str(obj)  # Convert any non-serializable objects to strings

    async def run_single_test(self, question: str) -> State:
        # Create initial state

        try:    
            initial_state = State(
                messages=[HumanMessage(content=question)]
            )
            
            final_state = await self.graph.ainvoke(initial_state)

        except Exception as e:
            print(f"Error processing question in agent: {str(e)}")
            return None

        runs = self.client.list_runs(project_name=self.project_name_langsmith, is_root=True)
        first_run = next(runs)

        execution_time = ""
        if first_run.end_time is not None and first_run.start_time is not None:
            execution_time = first_run.end_time - first_run.start_time
        else:
            print("Warning: Run has None value for start_time or end_time")
            execution_time = 0  # Default value

        # Get child runs to find sparql_query_construction run
        child_runs = list(self.client.list_runs(project_name=self.project_name_langsmith, parent_run_id=first_run.id))
        
        if isinstance(final_state, dict):
            structured_output = final_state.get("structured_output", {})
            if isinstance(structured_output, dict):
                query = structured_output.get("query", "")
            else:
                query = ""
        else:
            print(f"[run_single_test] Warning: final_state is not a dict. Type: {type(final_state)}, Value: {final_state}")
            structured_output = {}
            query = ""
        
        final_state_results = {
            "final_state_response": query,
            "run_id_langsmith": str(first_run.id),
            "execution_time": str(execution_time)
        }
        
        # Dynamically collect token usage for tracked nodes
        node_token_results = {}
        for run in child_runs:
            if run.name in self.tracked_token_nodes:
                key_prefix = run.name
                node_token_results[f"{key_prefix}"] = True
                node_token_results[f"{key_prefix}_prompt_tokens"] = run.prompt_tokens or 0
                node_token_results[f"{key_prefix}_completion_tokens"] = run.completion_tokens or 0
                node_token_results[f"{key_prefix}_total_tokens"] = run.total_tokens or 0
                # Optionally add cost metrics if needed
                # node_token_results[f"{key_prefix}_prompt_cost"] = run.prompt_cost or 0
                # node_token_results[f"{key_prefix}_completion_cost"] = run.completion_cost or 0
                # node_token_results[f"{key_prefix}_total_cost"] = run.total_cost or 0
        
        summed_result = {**final_state_results, **node_token_results}

        return summed_result

    async def run_all_tests(self):

        updated_results = []
        list_evaluated_queries = []
        list_evaluated_queries_including_empty_result = []
        list_evaluated_queries_excluding_empty_result = []
        syntactically_valid_queries_count = 0
        

        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        valid_metric_count_excluding_empty_result = 0
        valid_metric_count_including_empty_result = 0
        error_at_endpoint = 0
        empty_results_count = 0
        
        if self.test:
            test_dataset = self.test_dataset.select(range(1))
        else:
            test_dataset = self.test_dataset

        for i, item in enumerate(test_dataset):
            # Access the fields directly since we're using a Dataset object
            question = item["natural_language_question"]

            #print(question)
            if not question:
                print(f"Skipping item {i+1}/{len(test_dataset)} - no natural language question found")
                continue
            
            try:
                print("Processing item: " + str(item.get("file_path", "")))
                print(f"Sending question {i+1}/{len(test_dataset)} to agent...")
                result = await self.run_single_test(question)
                print(f"Got result for question {i+1}/{len(test_dataset)}")

                #print(result["final_state_response"])
                
                updated_item = {
                    # Meta data - access fields directly
                    "resource": item.get("resource", ""),
                    "natural_language_question": question,
                    "ground_truth_query": item.get("query", ""),
                    "target_endpoint": item.get("target_endpoint", ""),
                    "federates_with": item.get("federates_with", ""),
                    "endpoint_set": item.get("endpoint_set", ""),
                    "file_path": item.get("file_path", ""),
                    
                    # New data
                    "predicted_query": result["final_state_response"],
                    "predicted_endpoint": extract_endpoint_from_comment_regex(result["final_state_response"]),
                    "predicted_endpoint_equal_to_target_endpoint": normalize_url(extract_endpoint_from_comment_regex(result["final_state_response"])) == normalize_url(item.get("target_endpoint", "")),
                    "predicted_endpoint_in_federates_with": normalize_url(extract_endpoint_from_comment_regex(result["final_state_response"])) in [normalize_url(endpoint) for endpoint in item.get("federates_with", [])],
                    "predicted_endpoint_or_federated_endpoint": normalize_url(extract_endpoint_from_comment_regex(result["final_state_response"])) in [normalize_url(endpoint) for endpoint in item.get("federates_with", [])] or normalize_url(extract_endpoint_from_comment_regex(result["final_state_response"])) == normalize_url(item.get("target_endpoint", "")),
                    "run_id_langsmith": str(result["run_id_langsmith"]),
                    #"in_dataset": result["in_dataset"],
                    #"execution_time": str(result["execution_time"]),
                    #"prompt_tokens": result["prompt_tokens"],
                    #"completion_tokens": result["completion_tokens"],
                    #"total_tokens": result["total_tokens"],
                    #"prompt_cost": result["prompt_cost"],
                    #"completion_cost": result["completion_cost"],
                    #"total_cost": result["total_cost"],
                    "evaluation_timestamp": datetime.now().isoformat()
                }

                # Add token info for all tracked nodes dynamically
                if isinstance(result, dict):
                    for node in self.tracked_token_nodes:
                        if result.get(node):
                            updated_item[f"{node}_prompt_tokens"] = result.get(f"{node}_prompt_tokens")
                            updated_item[f"{node}_completion_tokens"] = result.get(f"{node}_completion_tokens")
                            updated_item[f"{node}_total_tokens"] = result.get(f"{node}_total_tokens")

                #########  Validate SPARQL syntax #########
                is_valid, error = validate_sparql_syntax(updated_item["predicted_query"])
                updated_item["is_valid_sparql"] = is_valid

                if not is_valid:
                    updated_item["sparql_syntax_error"] = error
                    updated_item["result_eval_f1_score"] = 0.0
                    updated_item["result_eval_precision"] = 0.0
                    updated_item["result_eval_recall"] = 0.0
                    updated_item["error_occured_at_endpoint"] = False
                    updated_item["predicted_query_result_is_empty"] = True
                    updated_item["ground_truth_query_result_is_empty"] = False
                    updated_item["error_occured_at_endpoint_message"] = "syntactically not correct"

                else:
                    updated_item["sparql_syntax_error"] = "syntactically correct"
                    syntactically_valid_queries_count += 1

                    df_ground_truth, df_predicted = format_query_result_dataframe(
                        ground_truth_query=updated_item["ground_truth_query"],
                        ground_truth_endpoint=updated_item["target_endpoint"],
                        predicted_query=updated_item["predicted_query"],
                        predicted_endpoint=updated_item["predicted_endpoint"],
                        timeout=self.timeout
                    )

                    # print("df_ground_truth:", df_ground_truth)
                    # print("df_predicted:", df_predicted)

                    # Initialize default values for all metrics and flags
                    updated_item["result_eval_f1_score"] = 0.0
                    updated_item["result_eval_precision"] = 0.0
                    updated_item["result_eval_recall"] = 0.0
                    updated_item["error_occured_at_endpoint"] = False
                    updated_item["predicted_query_result_is_empty"] = True
                    updated_item["ground_truth_query_result_is_empty"] = False
                    updated_item["error_occured_at_endpoint_message"] = ""

                    # Check if ground truth query resulted in an exception
                    if isinstance(df_ground_truth, Exception):
                        updated_item["ground_truth_query_result_is_empty"] = True
                        updated_item["error_at_ground_truth_endpoint"] = str(df_ground_truth)
                        updated_item["error_occured_at_endpoint_message"] = f"ground truth query error: {str(df_ground_truth)}"
                        # No metrics to calculate if ground truth is an exception
                    
                    # Check if predicted query resulted in an exception
                    elif isinstance(df_predicted, Exception):
                        gt_empty = getattr(df_ground_truth, "empty", True)
                        updated_item["error_occured_at_endpoint"] = True
                        updated_item["predicted_query_result_is_empty"] = True
                        updated_item["ground_truth_query_result_is_empty"] = gt_empty
                        updated_item["error_occured_at_endpoint_message"] = str(df_predicted)
                        error_at_endpoint += 1
                        # No metrics to calculate if predicted is an exception
                    
                    # Both queries executed without exception, calculate metrics
                    else:
                        # Both are valid DataFrames, calculate metrics
                        metrics = calculate_column_metrics_with_label_similarity(
                            file_path=item.get("file_path", ""), 
                            df_ground_truth=df_ground_truth, 
                            df_predicted=df_predicted
                        )
                        
                        # Update result metrics
                        updated_item["result_eval_precision"] = metrics["precision"]
                        updated_item["result_eval_recall"] = metrics["recall"]
                        updated_item["result_eval_f1_score"] = metrics["f1_score"]
                        
                        # Set flags based on metrics results
                        gt_empty = metrics.get("ground_truth_query_result_is_empty", False) #false for default value
                        pred_empty = metrics.get("predicted_query_result_is_empty", False)
                        
                        updated_item["ground_truth_query_result_is_empty"] = gt_empty
                        updated_item["predicted_query_result_is_empty"] = pred_empty
                        
                        # Case: Valid results with empty predicted
                        if not gt_empty and pred_empty:
                            updated_item["error_occured_at_endpoint_message"] = "no error, but empty result"
                            valid_metric_count_including_empty_result += 1
                            empty_results_count += 1
                            list_evaluated_queries_including_empty_result.append(item.get("file_path", ""))
                        
                        # Case: Valid results with non-empty predictions
                        elif not gt_empty and not pred_empty:
                            updated_item["error_occured_at_endpoint_message"] = "no error"
                            # Increment counters correctly - this query has results
                            valid_metric_count_excluding_empty_result += 1
                            valid_metric_count_including_empty_result += 1
                            list_evaluated_queries_excluding_empty_result.append(item.get("file_path", ""))
                            list_evaluated_queries_including_empty_result.append(item.get("file_path", ""))
                        
                        # Case: Empty ground truth but non-empty predicted 
                        elif gt_empty and not pred_empty:
                            updated_item["error_occured_at_endpoint_message"] = "ground truth empty, predicted query not empty"
                        
                        # Case: Both empty
                        elif gt_empty and pred_empty:
                            updated_item["error_occured_at_endpoint_message"] = "no error, but both ground truth and predicted query empty"
                        
                        # Update aggregate metrics
                        total_precision += metrics["precision"]
                        total_recall += metrics["recall"]
                        total_f1 += metrics["f1_score"]

                updated_results.append(updated_item)
                
            except Exception as e:
                print(f"Error processing question {i+1}/{len(test_dataset)}: {str(e)}")
                print("file_path:", item.get("file_path", ""))
                print("Offending item:", item)
                print("Stack trace:") 
                traceback.print_exc()
                
        
        self.updated_dataset = Dataset.from_list(updated_results)

        #########  SP-BLEU, METEOR metrics calculation #########
        evaluation_results = eval_pairs(zip(self.updated_dataset["ground_truth_query"], self.updated_dataset["predicted_query"]))
        
        # Initialize results dictionary with BLEU/METEOR metrics
        self.results_dict = {
            metric: value for metric, value in evaluation_results.items() 
                    if metric in ["SP-BLEU", "METEOR", "num_none_queries"]
        }
        
        # Add test metadata
        self.results_dict["size_of_test_set"] = len(self.updated_dataset)
        self.results_dict["error_at_endpoints"] = error_at_endpoint
        self.results_dict["empty_results_count"] = empty_results_count
        self.results_dict["syntactically_valid_queries_count"] = syntactically_valid_queries_count
        
        # Calculate and add metrics for both with and without empty results
        self.set_avg_metrics(
            self.results_dict, 
            "including_empty_result", 
            total_precision, 
            total_recall,
            total_f1,
            valid_metric_count_including_empty_result,
            list_evaluated_queries_including_empty_result
        )
        
        self.set_avg_metrics(
            self.results_dict, 
            "excluding_empty_result", 
            total_precision, 
            total_recall,
            total_f1,
            valid_metric_count_excluding_empty_result,
            list_evaluated_queries_excluding_empty_result
        )

        self.set_avg_metrics(
            self.results_dict, 
            "all", 
            total_precision, 
            total_recall,
            total_f1,
            len(self.updated_dataset),
            list_evaluated_queries
        )

        # Make results JSON-serializable
        self.results_dict = self.ensure_serializable(self.results_dict)

        # Save metrics to file
        with open(self.metric_dataset_path, 'w', encoding='utf-8') as f:
            json.dump(self.results_dict, f, indent=2, ensure_ascii=False)

        ######### Save evaluation dataset #########
        with open(self.evaluation_dataset_path, 'w', encoding='utf-8') as f:
            json.dump(self.updated_dataset.to_list(), f, indent=2, ensure_ascii=False)

        for item in self.updated_dataset:
            # Get the filename from the item or create one based on the resource
            if "filename" in item:
                filename = os.path.splitext(item["filename"])[0] + "_comparison.ttl"
            else:
                resource_id = item.get("resource", "").split("/")[-1]
                filename = f"{resource_id}_comparison.ttl"

            ######### Save comparison files #########
            save_queries_comparison(item.get("target_endpoint", ""),
                item.get("natural_language_question", ""),
                item.get("ground_truth_query", ""), 
                item.get("predicted_query", ""), 
                self.output_dir,
                filename
            )
        return self.evaluation_dataset_path
