import pandas as pd
from typing import Tuple, Dict, Any, Optional
from typing import Optional
from experiments.utilities.query_cache import cached_query_sparql
from entity_indexing.endpoint_loader import query_sparql_wrapper
import numpy as np
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity
import traceback
import json


def format_query_result_dataframe(
    ground_truth_query: str, 
    ground_truth_endpoint: str, 
    predicted_query: str, 
    predicted_endpoint: str,
    timeout: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    print("Querying ground truth endpoint...")

    ground_truth = cached_query_sparql(query = ground_truth_query, endpoint_url = ground_truth_endpoint, timeout=timeout)

    print("Querying predicted endpoint...")
    
    predicted = query_sparql_wrapper(predicted_query, predicted_endpoint, timeout=timeout)

    if isinstance(ground_truth, Exception):
       return ground_truth, predicted
    else:
        columns = ground_truth["head"]["vars"] 
        rows = []
        for binding in ground_truth["results"]["bindings"]:
            if not isinstance(binding, dict):
                print(f"[format_query_result_dataframe] Warning: Expected dict in ground_truth bindings, got {type(binding)}: {binding}")
                continue
            row = {col: binding.get(col, {}).get("value") for col in columns}
            rows.append(row)
        df_ground_truth = pd.DataFrame(rows, columns=columns)
        
    
    if isinstance(predicted, Exception):
        return ground_truth, predicted
    else:
        columns = predicted["head"]["vars"]
        rows = []
        for binding in predicted["results"]["bindings"]:
            if not isinstance(binding, dict):
                print(f"[format_query_result_dataframe] Warning: Expected dict in predicted bindings, got {type(binding)}: {binding}")
                continue
            row = {col: binding.get(col, {}).get("value") for col in columns}
            rows.append(row)
        df_predicted = pd.DataFrame(rows, columns=columns)
        
    return df_ground_truth, df_predicted


# old idea how to calculate metrics
# Chang argued it makes to many assumptions
# def calculate_column_metrics(df_ground_truth: pd.DataFrame, df_predicted: pd.DataFrame) -> Dict[str, float]:
#     if df_ground_truth.empty or df_predicted.empty:
#         return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
#     best_precision = 0.0
#     best_recall = 0.0
#     best_f1 = 0.0
    
#     for pred_col in df_predicted.columns:
#         pred_values = set(df_predicted[pred_col].dropna().astype(str))
#         if not pred_values:
#             continue
            
#         for gt_col in df_ground_truth.columns:
#             gt_values = set(df_ground_truth[gt_col].dropna().astype(str))
#             if not gt_values:
#                 continue
                
#             # Calculate true positives (intersection)
#             true_positives = len(pred_values.intersection(gt_values))
            
#             # Calculate precision, recall, F1
#             precision = true_positives / len(pred_values) if pred_values else 0
#             recall = true_positives / len(gt_values) if gt_values else 0
#             f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
#             # Update best scores
#             best_precision = max(best_precision, precision)
#             best_recall = max(best_recall, recall)
#             best_f1 = max(best_f1, f1)
    
#     return {
#         "precision": best_precision,
#         "recall": best_recall,
#         "f1_score": best_f1
#     }


def calculate_column_metrics_with_label_similarity(
    file_path,
    df_ground_truth: pd.DataFrame,
    df_predicted: pd.DataFrame,
    similarity_threshold: float = 0.7,
    embedding_cache_dir: str = "./embeddings_model_cache",
    embedding_model: str = "BAAI/bge-large-en-v1.5"   
) -> dict:

    print("[calculate_column_metrics_with_label_similarity] Calculating metrics for file:", file_path)


    gt_empty = getattr(df_ground_truth, "empty", True)
    pred_empty = getattr(df_predicted, "empty", True)
    
    if gt_empty and pred_empty:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0,
                "predicted_query_result_is_empty": True,
                "ground_truth_query_result_is_empty": True}
    elif gt_empty and not pred_empty:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0,
                "predicted_query_result_is_empty": False,
                "ground_truth_query_result_is_empty": True}
    elif pred_empty and not gt_empty:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0,
                "predicted_query_result_is_empty": True,
                "ground_truth_query_result_is_empty": False}

    

    gt_labels = list(df_ground_truth.columns)
    pred_labels = list(df_predicted.columns)

    gt_norm = {lbl.lower().strip(): lbl for lbl in gt_labels}
    pred_norm = {lbl.lower().strip(): lbl for lbl in pred_labels}

    exact_pairs = []
    for norm_lbl, gt_lbl in gt_norm.items():
        if norm_lbl in pred_norm:
            exact_pairs.append((gt_lbl, pred_norm[norm_lbl]))


    matched_gt = {gt for gt, _ in exact_pairs}
    matched_pred = {pred for _, pred in exact_pairs}

    remaining_gt = [lbl for lbl in gt_labels if lbl not in matched_gt]
    remaining_pred = [lbl for lbl in pred_labels if lbl not in matched_pred]

    print("exact pairs:", len(exact_pairs))
    print("remaining gt:", len(remaining_gt))
    

    sim_pairs = []
    if remaining_gt and remaining_pred:
        model = TextEmbedding(
            model_name=embedding_model,
            cache_dir=embedding_cache_dir
        )
        gt_embeds = np.vstack(list(model.embed(remaining_gt)))
        pred_embeds = np.vstack(list(model.embed(remaining_pred)))
        sim_matrix = cosine_similarity(gt_embeds, pred_embeds)

        used_pred_idx = set()
        for i, gt_lbl in enumerate(remaining_gt):
            # highest‑to‑lowest similarity indices
            
            for j in np.argsort(sim_matrix[i])[::-1]:

                print(f"{gt_lbl} -> {remaining_pred[j]} (similarity: {sim_matrix[i, j]})")

                if sim_matrix[i, j] < similarity_threshold or j in used_pred_idx:
                    continue
                # mutual‑best check
                if np.argmax(sim_matrix[:, j]) == i:
                    sim_pairs.append((gt_lbl, remaining_pred[j]))
                    used_pred_idx.add(j)
                    break  # move to next gt_lbl

    matches = exact_pairs + sim_pairs
    #print(matches)
    if not matches:
        print("no matches found")
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    gt_matched_cols = [gt for gt, _ in matches]
    pred_matched_cols = [pred for _, pred in matches]

    gt_tuples = set()
    for row in df_ground_truth[gt_matched_cols].astype(str).fillna("").values.tolist():
        gt_tuples.add(tuple(row))

    pred_tuples = set()
    for row in df_predicted[pred_matched_cols].astype(str).fillna("").values.tolist():
        pred_tuples.add(tuple(row))
        
    print("gt_tuples:", list(gt_tuples)[:1])
    print("pred_tuples:", list(pred_tuples)[:1])
    
    if not gt_tuples or not pred_tuples:
        print("no tuples found")
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    tp = len(gt_tuples & pred_tuples)
    precision = tp / len(pred_tuples)
    recall = tp / len(gt_tuples)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return {"precision": precision, "recall": recall, "f1_score": f1, "predicted_query_result_is_empty": False, "ground_truth_query_result_is_empty": False}