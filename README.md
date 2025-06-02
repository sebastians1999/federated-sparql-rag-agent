
# Evaluating Prompting Methodologies for Generating Federated SPARQL Queries over Biomedical Knowledge Graphs

## Overview

This repository contains the implementation of an RAG-based system for generating federated SPARQL queries from natural language questions over biomedical knowledge graphs. The system evaluates five different prompting methodologies (Baseline, CP, CP-A, CoT, LtM) using a modular pipeline architecture.

## 📁 Repository Structure
```              
├── README.md                
├── endpoint_indexing/       
│   └── [endpoint indexing code]
├── entity_indexing/        
│   
├── experiments/    
│   ├── experiment_data/
│   ├── experiment_runner_functions/
│   ├── federated_sparql_dataset/
│   │   └── examples_federated_19.04.2025/
│   │       ├── Bgee/
│   │       ├── OMA/
│   │       ├── OrthoDB/
│   │       ├── Rhea/
│   │       ├── SwissLipids/
│   │       ├── UniProt/
│   │       ├── dbgi/
│   │       ├── neXtProt/
│   │       └── sparql-examples-ontology.ttl
│   └── utilities/
│
├── jupyter_notebooks/       
│   ├── dataset_analysis/
│   ├── evaluation_notebooks/
│   ├── experiment_development_notebooks/
│   └── system_development_notebooks/
│
├── scr/                     
│   ├── agent/               
│   │   ├── nodes/         
│   │   ├── prompts/        
│   │   ├── state/          
│   │   └── utils/          
│   │       ├── config.py 
│   │       ├── llm_utils.py
│   │       └── graph.py              
│   └── vectordb/           
└── tests/     
```
## Methodologies

- **Baseline**: Simple prompt with minimal instructions.
- **CP (Construction Prompt)**: Structured prompt with explicit federated SPARQL instructions and endpoint descriptions.
- **CP-A (Augmented Construction Prompt)**: CP enhanced with dynamically retrieved example question-SPARQL query pairs.
- **CoT (Chain-of-Thought)**: CP with vanilla "Think step by step" phrase at th end of the prompt.
- **few-shot CoT (few-shot Chain-of-Thought)**: Step-by-step few-shot CoT examples, with comprehensive 12-step guidance process.
- **LtM (Least-to-Most)**: Decompositional approach that breaks query generation into three sub-problems: planning, triple pattern generation with validation, and final assembly.


**Note:** All prompts to the corresponding prompting strategies can be found in `scr/agent/prompts`.

## Dataset

This system is evaluated on a curated dataset of federated SPARQL queries over biomedical knowledge graphs. The evaluation focuses on complex queries that span multiple endpoints in the life sciences domain.


### Key aspects

- **Source**: human-written natural language questions paired with their corresponding SPARQL queries, including federated queries, over biomedical KGs [Bolleman et al. (2024)](https://arxiv.org/abs/2410.06010).

- **Covered SPARL endpoints**: 32 valid (checked for validity) federated SPARQL queries across three primary endpoints:

    - **[UniProt](https://sparql.uniprot.org/sparql/)** - Protein sequence and functional annotation data
    - **[Rhea](https://sparql.rhea-db.org/sparql/)** - Biochemical reactions using ChEBI ontology  
    - **[SwissLipids](https://beta.sparql.swisslipids.org/)** - Curated lipidomics knowledge base

The datset can be found here: `experiments/federated_sparql_dataset/examples_federated_19.04.2025`.



## 🚀 Getting Started

### Requirements

- Python 3.11 or higher
- pip (package installer for Python)
- Docker

### Installation

1. Clone the Repository
```bash
git clone https://github.com/sebastians1999/federated-sparql-rag-agent.git
cd federated-sparql-rag-agent
```


2. Create and activate a virtual environment


```bash
# MacOS
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate
```


3. Install the required dependencies.
 ```bash
pip install -e .
   ```

4. Create a .env file in the root directory of the repository to store your API keys securely. This file should contain your LLM provider API keys. Optionally, you can also add a Langsmith API key for enhanced agent tracking and monitoring. 
 ```bash
#Optional
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://eu.api.smith.langchain.com"
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

GOOGLE_API_KEY = 
```
**Note:** the following providers are supported:
- OpenAI
- TogetherAI
- Groq
- Google Gemini
- Anthropic
Please have a look at the `scr/agent/utils/config.py` file to see examples how the providers can be set. If you would like to use a provider that is not listed here, please have a look at `scr/agent/utils/llm_utils.py` and the functionality accordingly (orientage on the other providers).


5. The system can be configured by editing the configuration file in `scr/agent/utils/config.py` directory. Here it is possible to configure LLM settings (provider, models, temperatures, ect.), RAG settings (embbeding models for retrieval, top_k, collection, ect.) and what meta data shall be tracked for experimental runs.


## Usage

### 1. Start Vector Database with with Docker Compose
 ```bash
cd scr/vectordb
docker-compose up -d qdrant
```

This will:

- Start Qdrant on ports 6333 (HTTP) and 6334 (gRPC)
- Create persisten storage in `./data/qdrant/`
- Use the configuration from `qdrant_config.yml`
- Allocate up to 2 CPUs and 4GB RAM


### 2. Index entity URIs and SPARQL question pairs

Before running the agent, you need to index entity URIs and depending on what methodologies you would like to evaluate, question-SPARQL pairs, too. 


#### Index Entity URIs

The entites to be indexed are predefined in `entity_indexing/entities_collection.py` and focus on endpoints from the evaluation set, which comprises federated SPARQL queries from Uniprot, Rhea and SwissLipids `experiments/federated_sparql_dataset/examples_federated_19.04.2025`.

 ```bash
python entity_indexing/entity_indexing.py

# Or with custom configuration
python entity_indexing/entity_indexing.py \
  --host localhost \
  --grpc-port 6334 \
  --collection entities_collection \
  --dense-model BAAI/bge-small-en-v1.5 \
  --workers 4 \
  --batch-size 144 \
  --recreate False \
  --log-dir ./upload_logs
```
**Note:** Entities are indexed using FastEmbed, using no GPU. Thus depending on what setup you have please set the number of workers higher to speed things up. Otherwise this process might take a while. The entity indexing uses logging. So if something should happen you can just run the command again and it will continue from where it stopped. 


#### Index question-SPARQL pairs
 ```bash
# Basic examples indexing with default settings (from project root)
python endpoint_indexing/endpoint_indexing.py

# Or with custom configuration
python endpoint_indexing/endpoint_indexing.py \
    --host localhost \
    --port 6333 \
    --collection biomedical_examples_collection_v1.0 \
    --model BAAI/bge-large-en-v1.5 \
    --parallel 4
```


### 3. SPARQL Query Result Caching (Optional)

Since most of the SPARQL queries in the evaluation set are highly complex, executing them can sometimes take a long time. 
Although caching the results of the ground truth SPARQL queries is part of the evaluation pipeline to shorten future runs, it might be more efficient to cache them once before running experiments. Per default all (32) SPARQL queries of the evaluation set are cached. The cached results can be found in the following directory `experiments/federated_sparql_dataset/query_cache` (once at least one query result is cached). Every cached query gets a UUID that corresponds to the cached federated SPARQL query. Modify the script if would like to only index certain queries or for additional endpoints (`endpoint_files_map={"UniProt": [],"Rhea": [],"SwissLipids": []}` to e.g. `endpoint_files_map={"SwissLipids": [6.ttl]}`)

 ```bash
python experiments/utilities/cache_queries.py
```



### 4. Choose Methodology

In `scr/agent/utils/graph.py` you can choose between different prompting strategies. Depending on which methodology you would like to use, please uncomment the corresponding section. **LtM** is set per default.

### 5. Run Evaluation and Agent


Evaluations for different methodologies can be done in form of a single experimental run and multi experimental runs. Multi-run evaluations account for the inherent variability in LLM outputs, which can cause performance fluctuations even under consistent experimental settings.

Both functions to run the evaluation pipelines can be found in `experiments/experiment_runner_functions`

**Note**: With `endpoint_sets = {"SwissLipids": [], "Uniprot": [], "Rhea": []}` all federated SPARQL queries (32) of these endpoints are evaluated. Assuming you would like to run the evaluation pipeline for certain queries of the evaluation set you can do this by providing the specific file name of that query: `endpoint_sets = {"SwissLipids": [6.ttl], "Uniprot": [42_connect_patents_to_epo.ttl, 49_tissues_where_genes_metabolizing_cholestrol_are_expressed.ttl], "Rhea": []}` If you would like to evaluate federated SPARQL queries from different endpoints (e.g. Bgee) you can add the desired endpoint simply to the `endpoint_sets = {"Bgee": []}`

**🚨 CAUTION 🚨**: 
- Only queries in SwissLipids, UniProt and Rhea are part of the evaluation set and are validated for syntactically and semantically validity.
- If you would like to evaluate few-shot CoT you **must** exclude the few-shot examples `{"SwissLipids": [5.ttl], "Uniprot": [40_human_enzymes_that_metabolize_sphingolipidsl], "Rhea": [94_Select_all_approved_reactions_with_CHEBI_or_one_of_its_descendant_optional_UniProtKB_reviewed_EC.ttl]}` from the evaluation set. Otherwise the evaluation gets biased as the Agent would get these queries correct every time. 




#### Single experimental run

 ```bash
python experiments/experiment_runner_functions/run_agent_evaluation.py


# Modify these parameters  in the script as needed
endpoint_sets = {"SwissLipids": [], "Uniprot": [], "Rhea": []} 
experiment_dir = "experiments/experiment_data"
project_name = "your_experiment_name"
timeout = 300
tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
dataset_dir = "path/to/your/dataset"
```

#### Multi experimental run

 ```bash
python experiments/experiment_runner_functions/run_multi_evaluation.py


# Modify these parameters in the script as needed
num_runs = 10  
endpoint_sets = {"SwissLipids": [], "Uniprot": [], "Rhea": []}
experiment_dir = "experiments/experiment_data"
project_name = "your_multi_run_experiment"
timeout = 600 (10 mins)
tracked_token_nodes = ["question_understanding", "planning", "pattern", "assembler"]
dataset_dir = "path/to/your/dataset"
```

All experimental runs are saved with a time-stamp to the following directory `experiments/experiment_data`, unless you change it.
To get insights you can go to the jupyter notebooks `multi_run_evaluation.ipynb` and `single_run_evaluation` in the directory `jupyter_notebooks/evaluation_notebooks`. 
As this work is part of a Bachelor Thesis, there has been done a comprehensive evaluation of the proposed prompting methdologies. These insights can be seen in these notebooks. If you would like to try your own methodologies feel free to add and compare them here. 

## Additional Information

During the development of this repository a number of notebooks were created. Not only for deveopment and prototyping, but also to validate approaches (e.g. what is the best approach for column matching in the evaluation framework), or for analysis of results. All these notebooks can be found in the directory `jupyter_notebooks`. In this directory you can find another README file, detailing what these notebooks contain.


## Experiment Logs Overview

**Note**: Experiment prefixed with `multi_run_` represent 10 independent trials for statistical analysis. Experiment prefixes with `ev_`are single experimental runs of the evaluation set (32 federated SPARQL queries).



| Name | Variant | LLM Model | Temperature |
|------|---------|-----------|-------------|
| ev_2025-04-21_18-31-20 | Baseline | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_02-04-22 | Baseline | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-23_11-26-44 | CP | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_16-27-37 | CP | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-22_17-38-49 | CoT (Baseline) | gemini 2.0 flash | 0.8 |
| ev_2025-04-22_21-44-48 | CoT (CP) | gemini 2.0 flash | 0.8 |
| ev_2025-04-23_10-26-29 | CoT (CP) | gemini 2.5 flash (no thinking) | 0.8 |
| ev_2025-04-25_16-58-55 | CoT (CP) | gemini 2.0 flash | 0.1 |
| ev_2025-04-25_17-49-29 | CP | gemini 2.0 flash | 0.1 |
| ev_2025-04-26_16-52-04 | few-shot CoT | gemini 2.0 flash | 0.1 |
| ev_2025-04-26_18-21-19 | CoT (CP) | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-04-27_15-06-28 | few-shot CoT | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-04-27_16-18-37 | few-shot CoT | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-04-27_17-31-27 | few-shot CoT | gemini 2.0 flash | 0.1 |
| ev_2025-04-27_19-52-47 | few-shot CoT | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-04-30_18-18-41 | CP-A | gemini 2.0 flash | 0.1 |
| ev_2025-05-01_09-04-25 | CP-A | gemini 2.5 flash (no thinking) | 0.1 |
| ev_2025-05-01_11-36-06 | CP-A | gemini 2.5 flash (thinking) | 0.1 |
| ev_2025-05-01_13-24-50 | CP-A | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-02_00-31-21 | CP-A | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-04_00-51-30 | few-shot CoT | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-06_22-14-46 | LtM | gemini 2.0 flash | 0.1 |
| ev_2025-05-08_18-12-10 | Baseline | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-10_14-26-00 | Baseline | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-10_18-05-54 | CP | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-11_00-21-16 | CoT (CP) | gemini 2.0 flash | 0.1 |
| multi_run_2025-05-25_17-14-57 | LtM | gemini 2.5 flash (thinking) | 0.1 |


## 📫 Contact

s.schmulling@student.maastrichtuniversity.nl


## License

MIT License

Copyright (c) 2025 Sebastian Schmülling

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


