import asyncio
import sys
import os
import time
from datetime import datetime
import dotenv
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
from experiments.utilities.result_metric import format_query_result_dataframe, calculate_column_metrics



class AgentEvaluator:
    def __init__(self, dataset_path=None, output_dir=None, endpoint_sets=None, project_name_langsmith: str ="sparql-rag-agent", test: bool = False, experiment_dir: str = None):
        
        self.endpoint_sets = endpoint_sets
        self.experiment_dir = experiment_dir
        self.output_dir = process_specific_datasets_and_files(self.endpoint_sets, output_dir=self.experiment_dir)
        self.test_dataset_path = os.path.join(self.output_dir, 'testset_meta_data.json')
        self.test_dataset = Dataset.from_dict(load_data_from_file(self.test_dataset_path))
        self.graph = create_graph()
        self.client = Client()
        self.project_name_langsmith = project_name_langsmith
        self.results = []
        self.evaluation_dataset_path = os.path.join(self.output_dir, 'evaluation_dataset.json')
        self.metric_dataset_path = os.path.join(self.output_dir, 'metrics_dataset.json')
        self.test = test

        
    async def run_single_test(self, question: str) -> State:
        # Create initial state

        try:    
            initial_state = State(
                messages=[HumanMessage(content=question)]
            )
            
            final_state = await self.graph.ainvoke(initial_state)
            print(final_state)
        except Exception as e:
            print(f"Error processing question in agent: {str(e)}")
            return None

        runs = self.client.list_runs(project_name=self.project_name_langsmith, is_root=True)
        first_run = next(runs)
        print("Got first run!")

        # Handle None values for datetime fields
        execution_time = ""
        if first_run.end_time is not None and first_run.start_time is not None:
            execution_time = first_run.end_time - first_run.start_time
        else:
            print("Warning: Run has None value for start_time or end_time")
            execution_time = 0  # Default value

        # Get child runs to find sparql_query_construction run
        child_runs = list(self.client.list_runs(project_name=self.project_name_langsmith, parent_run_id=first_run.id))
        
        # Filter to find the sparql_query_construction run
        sparql_construction_run = None
        for run in child_runs:
            if run.name == "sparql_query_construction":
                sparql_construction_run = run
                break

        if sparql_construction_run:
            result = {
                "final_state_response": final_state.get("structured_output", {}).get("query", ""),
                "run_id_langsmith": str(first_run.id),
                "in_dataset": first_run.in_dataset,
                "execution_time": str(execution_time),

                # Add the specific metrics for the sparql_query_construction run
                "sparql_construction_prompt_tokens": sparql_construction_run.prompt_tokens or 0,
                "sparql_construction_completion_tokens": sparql_construction_run.completion_tokens or 0,
                "sparql_construction_total_tokens": sparql_construction_run.total_tokens or 0,
                "sparql_construction_prompt_cost": sparql_construction_run.prompt_cost or 0,
                "sparql_construction_completion_cost": sparql_construction_run.completion_cost or 0,
                "sparql_construction_total_cost": sparql_construction_run.total_cost or 0,
                

                # Keep the original metrics too
                "prompt_tokens": first_run.prompt_tokens or 0,
                "completion_tokens": first_run.completion_tokens or 0,
                "total_tokens": first_run.total_tokens or 0,
                "prompt_cost": first_run.prompt_cost or 0,
                "completion_cost": first_run.completion_cost or 0,
                "total_cost": first_run.total_cost or 0,
            }
        else:
            print("Warning: Could not find the sparql_query_construction run")
            # Fall back to using the parent run metrics
            result = {
                "final_state_response": final_state.get("structured_output", {}).get("query", ""),
                "run_id_langsmith": str(first_run.id),
                "in_dataset": first_run.in_dataset,
                "execution_time": str(execution_time),
                "prompt_tokens": first_run.prompt_tokens or 0,
                "completion_tokens": first_run.completion_tokens or 0,
                "total_tokens": first_run.total_tokens or 0,
                "prompt_cost": first_run.prompt_cost or 0,
                "completion_cost": first_run.completion_cost or 0,
                "total_cost": first_run.total_cost or 0,
            }
            
        print("Result:", result)

        return result

    async def run_all_tests(self):

        updated_results = []
        count_total_processed_result_eval = 0
        

        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        valid_metric_count = 0
        
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
                print(f"Sending question {i+1}/{len(test_dataset)} to agent...")
                result = await self.run_single_test(question)
                print("Got result")
                
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
                    
                    "run_id_langsmith": str(result["run_id_langsmith"]),
                    "in_dataset": result["in_dataset"],
                    "execution_time": str(result["execution_time"]),
                    "prompt_tokens": result["prompt_tokens"],
                    "completion_tokens": result["completion_tokens"],
                    "total_tokens": result["total_tokens"],
                    "prompt_cost": result["prompt_cost"],
                    "completion_cost": result["completion_cost"],
                    "total_cost": result["total_cost"],
                    "evaluation_timestamp": datetime.now().isoformat()
                }

                if "sparql_construction_prompt_tokens" in result:
                    updated_item["sparql_construction_prompt_tokens"] = result["sparql_construction_prompt_tokens"]
                    updated_item["sparql_construction_completion_tokens"] = result["sparql_construction_completion_tokens"]
                    updated_item["sparql_construction_total_tokens"] = result["sparql_construction_total_tokens"]
                    updated_item["sparql_construction_prompt_cost"] = result["sparql_construction_prompt_cost"]
                    updated_item["sparql_construction_completion_cost"] = result["sparql_construction_completion_cost"]
                    updated_item["sparql_construction_total_cost"] = result["sparql_construction_total_cost"]


                #########  Validate SPARQL syntax #########
                is_valid, error = validate_sparql_syntax(updated_item["predicted_query"])
                updated_item["is_valid_sparql"] = is_valid
                updated_item["sparql_syntax_error"] = error

                #########  Result comparison metrics calculation #########
                df_ground_truth, df_predicted = format_query_result_dataframe(
                    ground_truth_query=updated_item["ground_truth_query"],
                    ground_truth_endpoint=updated_item["target_endpoint"],
                    predicted_query=updated_item["predicted_query"],
                    predicted_endpoint=updated_item["predicted_endpoint"]
                )

                # In theory there should be no more test instances where the result of the query is empty because I filtered them out. 
                # So this is a sanity check to not corrupt the metric. 
                if df_ground_truth.empty:
                    updated_item["ground_truth_query_result_is_empty"] = True
                else: 
                    updated_item["ground_truth_query_result_is_empty"] = False
                
                    if df_predicted.empty:
                        updated_item["result_eval_f1_score"] = 0.0
                        updated_item["result_eval_precision"] = 0.0
                        updated_item["result_eval_recall"] = 0.0
                    else:
                        metrics = calculate_column_metrics(df_ground_truth, df_predicted)
                        updated_item["result_eval_precision"] = metrics["precision"]
                        updated_item["result_eval_recall"] = metrics["recall"]
                        updated_item["result_eval_f1_score"] = metrics["f1_score"]
                        
                        # aggregate metrics
                        total_precision += metrics["precision"]
                        total_recall += metrics["recall"]
                        total_f1 += metrics["f1_score"]
                        valid_metric_count += 1

                updated_results.append(updated_item)
                
            except Exception as e:
                print(f"Error processing question {i+1}/{len(test_dataset)}: {str(e)}")
        
        self.updated_dataset = Dataset.from_list(updated_results)
 

        #########  SP-BLEU, METEOR metrics calculation #########
        evaluation_results = eval_pairs(zip(self.updated_dataset["ground_truth_query"], self.updated_dataset["predicted_query"]))
        
        self.results_dict = {
            metric: value for metric, value in evaluation_results.items() 
                if metric in ["SP-BLEU", "METEOR", "num_none_queries"]
        }
        self.results_dict["num_pairs_evaluated"] = len(self.updated_dataset)
        
        # Add aggregate result metrics to results_dict
        if valid_metric_count > 0:
            self.results_dict["avg_result_precision"] = total_precision / valid_metric_count
            self.results_dict["avg_result_recall"] = total_recall / valid_metric_count
            self.results_dict["avg_result_f1"] = total_f1 / valid_metric_count
        else:
            self.results_dict["avg_result_precision"] = 0.0
            self.results_dict["avg_result_recall"] = 0.0
            self.results_dict["avg_result_f1"] = 0.0


        with open(self.metric_dataset_path, 'w', encoding='utf-8') as f:
            json.dump(self.results_dict, f, indent=2, ensure_ascii=False)

        #########  Save evaluation dataset #########
        with open(self.evaluation_dataset_path, 'w', encoding='utf-8') as f:
            json.dump(self.updated_dataset.to_list(), f, indent=2, ensure_ascii=False)

        for item in self.updated_dataset:
            # Get the filename from the item or create one based on the resource
            if "filename" in item:
                filename = os.path.splitext(item["filename"])[0] + "_comparison.ttl"
            else:
                resource_id = item.get("resource", "").split("/")[-1]
                filename = f"{resource_id}_comparison.ttl"

            #########  Save comparison files #########
            save_queries_comparison(item.get("target_endpoint", ""),
                item.get("natural_language_question", ""),
                item.get("ground_truth_query", ""), 
                item.get("predicted_query", ""), 
                self.output_dir,
                filename
            )
        return self.evaluation_dataset_path