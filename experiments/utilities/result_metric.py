import pandas as pd
from typing import Tuple, Dict, Any, Optional
from typing import Optional
from experiments.utilities.query_cache import cached_query_sparql
from entity_indexing.endpoint_loader import query_sparql


def format_query_result_dataframe(
    ground_truth_query: str, 
    ground_truth_endpoint: str, 
    predicted_query: str, 
    predicted_endpoint: str,
    timeout: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:


    ground_truth = cached_query_sparql(query = ground_truth_query, endpoint_url = ground_truth_endpoint, timeout=timeout)
    predicted = query_sparql(predicted_query, predicted_endpoint, timeout=timeout)

    if ground_truth == 'error':

        df_ground_truth = pd.DataFrame()
    else:
        processed_data = []
        bindings_ground_truth = ground_truth['results']['bindings']
        for row_binding in bindings_ground_truth:
            processed_row = {}
            for var_name, value_dict in row_binding.items():
                if isinstance(value_dict, dict) and 'value' in value_dict:
                    processed_row[var_name] = value_dict['value']
                else:
                    processed_row[var_name] = None
            processed_data.append(processed_row)
        df_ground_truth = pd.DataFrame(processed_data)
    
    if predicted == 'error':
        df_predicted = pd.DataFrame()
    else:
        processed_data = []
        bindings_predicted = predicted['results']['bindings']
        for row_binding in bindings_predicted:
            processed_row = {}
            for var_name, value_dict in row_binding.items():
                if isinstance(value_dict, dict) and 'value' in value_dict:
                    processed_row[var_name] = value_dict['value']
                else:
                    processed_row[var_name] = None
            processed_data.append(processed_row)
        df_predicted = pd.DataFrame(processed_data)
        
    return df_ground_truth, df_predicted


def calculate_column_metrics(df_ground_truth: pd.DataFrame, df_predicted: pd.DataFrame) -> Dict[str, float]:
    if df_ground_truth.empty or df_predicted.empty:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
    best_precision = 0.0
    best_recall = 0.0
    best_f1 = 0.0
    
    for pred_col in df_predicted.columns:
        pred_values = set(df_predicted[pred_col].dropna().astype(str))
        if not pred_values:
            continue
            
        for gt_col in df_ground_truth.columns:
            gt_values = set(df_ground_truth[gt_col].dropna().astype(str))
            if not gt_values:
                continue
                
            # Calculate true positives (intersection)
            true_positives = len(pred_values.intersection(gt_values))
            
            # Calculate precision, recall, F1
            precision = true_positives / len(pred_values) if pred_values else 0
            recall = true_positives / len(gt_values) if gt_values else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            # Update best scores
            best_precision = max(best_precision, precision)
            best_recall = max(best_recall, recall)
            best_f1 = max(best_f1, f1)
    
    return {
        "precision": best_precision,
        "recall": best_recall,
        "f1_score": best_f1
    }