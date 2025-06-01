

# Notebook Collection

## Overview

```bash
├── jupyter_notebooks/       
│   ├── dataset_analysis/
│   │   ├── dataset_analysis_notebook.ipynb
│   │   └── plots_dataset_analysis/
│   │
│   ├── evaluation_notebooks/
│   │   ├── experiment_comparison.ipynb
│   │   ├── multi_run_evaluation.ipynb
│   │   ├── single_run_evaluation.ipynb
│   │   └── multi_experimental_run_plots/
│   │
│   ├── experiment_development_notebooks/
│   │   ├── federated_test_set_evaluation.ipynb
│   │   ├── prototyping.ipynb
│   │   └── system_test_runner.ipynb
│   │
│   └── system_development_notebooks/
│       ├── column_matching_dev_notebook.ipynb
│       ├── cot_prompt_engineering.ipynb
│       ├── endpoint_indexing.ipynb
│       ├── entity_loading.ipynb
│       ├── retrieval_eval.ipynb
│       ├── sparql_query_result_evaluation_dev.ipynb
│       └── sparql_query_validator.ipynb
```


## Dataset Analysis

#### `dataset_analysis_notebook.ipynb`
```
Analyzes the federated SPARQL dataset, including query structures, endpoints, and similarities between queries.
```

## Evaluation Notebooks

#### `experiment_comparison.ipynb`
```
Compares results across different experimental runs and methodologies. This notebook was only used for initial investigations and ideation. The final results can be found in multi_run_evaluation.ipynb or single_run_evaluation.ipynb, which can be found in the same directory as this file. However, it shows interesting clues about performance and also includes the performance from different LLMs. 
```

#### `multi_run_evaluation.ipynb`
```
Analyzes results from multi experimental runs (10 experimental runs), calculating statistics and performance metrics with visualizations. These visualizations can also be found in the Bachelor Thesis.
```

#### `single_run_evaluation.ipynb`
```
Evaluates single experimental runs with visualizations.
```

## Experiment Development

#### `federated_test_set_evaluation.ipynb`
```
In this notebook the SPARQL queries of the evaluation set were evaluated for errors. After this analysis the corresponding queries were excluded from the evaluation set, leaving a total of 32 federated SPARQL queries. Additionally, the evaluation set was cached to speed up the evaluation pipeline.
```

#### `prototyping.ipynb`
```
Development notebook, used for developing and testing new experimental approaches.
```

#### `system_test_runner.ipynb`
```
Was used to perform single and multi experimental runs. Rather than running the command line this notebook was used to run experiments from this notebook. Furthermore it contains plots that show the variability of F1, precision and recall for a 10 experimental run (one multi run).
Additionally for each multi run statistics were aggregated that are stored as meta data for each experiment directory prefixed with `multi_run_`.
```

## System Development

#### `column_matching_dev_notebook.ipynb`
```
Develops and tests column matching algorithms for query result comparison.
```

#### `cot_prompt_engineering.ipynb`
```
Experiments with Chain-of-Thought (CoT) prompt engineering and formatting.
```

#### `endpoint_indexing.ipynb`
```
Development notebook of functionality for indexing and querying SPARQL endpoints.
```

#### `entity_loading.ipynb`
```
Handles entity URI indexing, loading and preprocessing. This notebook was also used for experimental purposes (e.g. to track how long it takes to load entites for certain endpoints).
```

#### `retrieval_eval.ipynb`
```
Evaluation notebook for retrieval components of the RAG system.
```

#### `sparql_query_result_evaluation_dev.ipynb`
```
Development notebook for SPARQL query result evaluation metrics.
```

#### `sparql_query_validator.ipynb`
```
Development notebook for the SPARQL syntax validator (part of the evaluation framework).
```
