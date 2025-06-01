from .general import INTRODUCTION_PROMPT



QUERY_PLANNING_PROMPT = (
    INTRODUCTION_PROMPT
    + """
Identified entities and classes from the user question {{entities_question}} {{classes_question}}
   
Potential entities extracted from the user question {{potential_entities}}

Potential classes extracted from the user question  {{potential_classes}}

Example queries (**Note:** These queries are examples of a natural questions with a corresponding sparql query. They may be not federated, but give hints about how the schema of an endpoint look like) {{extracted_example_queries}}

The following are SPARQL endpoint descriptions where the federated sparql query can be executed on or can federate with: 

---
UniProt SPARQL
https://sparql.uniprot.org/sparql

A comprehensive endpoint containing triples of protein-related data, providing access to protein sequences, functional annotations, and cross-references, making it essential for querying protein information and their biological functions.
---
Rhea DB SPARQL
https://sparql.rhea-db.org/sparql

An expert-curated endpoint containing biochemical reactions that uses ChEBI ontology for chemical entities, allowing users to query detailed information about enzymatic reactions, transport reactions, and spontaneous reactions in biological systems.
---
SwissLipids SPARQL
https://sparql.swisslipids.org/sparql/

A specialised endpoint containing lipid structures that provides detailed information about lipid biology, including lipid classifications, metabolic reactions, and associated enzymes, making it valuable for lipidomics research and lipid-related queries.
---

**Task:**

– **Map identified entties or classes from the user question to ontology IRIs that are needed to build the sparql query** (If there is not a good match in the provided context (potential entities, potential classes, example queries) figure out a mapping from your knowledge)

– Determine return labels (early draft `SELECT` vars) 

– Locate **SPARQL endpoints** we will need to answer the question and what information we seek to retrieve from that endpoint.

– Choose the **primary endpoint** where the query is going to be executed.

**Example Output:**

QueryPlan(
    "iri_map": {
        "Alzheimer's Disease": "http://example.org/ontology/Disease_123",
        "APP gene": "http://example.org/ontology/Gene_456"
    },
    "early_select": ["?disease", "?gene"],
    "federated_endpoints": [
        "https://sparql.rhea-db.org/sparql",
        "https://sparql.uniprot.org/sparql"
    ],
    "target_endpoint": "https://sparql.uniprot.org/sparql"
)
"""
)


UNIPROT_DESCRIPTION_QUERY = """
UniProt SPARQL
https://sparql.uniprot.org/sparql

A comprehensive endpoint containing triples of protein-related data, providing access to protein sequences, functional annotations, and cross-references, making it essential for querying protein information and their biological functions.
"""

RHEA_DESCRIPTION_QUERY = """
Rhea DB SPARQL
https://sparql.rhea-db.org/sparql

An expert-curated endpoint containing biochemical reactions that uses ChEBI ontology for chemical entities, allowing users to query detailed information about enzymatic reactions, transport reactions, and spontaneous reactions in biological systems.
"""

SWISSLIPIDS_DESCRIPTION_QUERY = """
SwissLipids SPARQL
https://sparql.swisslipids.org/sparql/

A specialised endpoint containing lipid structures that provides detailed information about lipid biology, including lipid classifications, metabolic reactions, and associated enzymes, making it valuable for lipidomics research and lipid-related queries.
"""





QUERY_PATTERN_PROMPT_SERVICE_BLOCK = (
    INTRODUCTION_PROMPT
    + """
**Task**

You are writing **one remote SERVICE block** for a federated SPARQL query.  
For the endpoint shown in *Endpoint for this block* you must output **exactly one** self‑contained snippet that:

* lists every `PREFIX` required by the snippet,
* wraps the triple pattern(s) inside **`SERVICE <{{service_endpoint}}> { … }`**,
* is itself wrapped in `ASK WHERE { … }` so we can test it quickly.

The block will not answer the user question on its own; its job is to fetch **partial information** that the primary endpoint (`{{target_endpoint}}`) will later join with other blocks.  
Be reasonable about the amount and granularity of data you pull from this remote endpoint.

---

**Requirements**

1. **Exactly one block** – shape:  
   `PREFIX … ASK WHERE { SERVICE <{{service_endpoint}}> { … } }`
2. **Use the IRI bindings** given in *Mapping* exactly (or IRIs from the examples); do not invent IRIs. 
3. **Keep it minimal but meaningful**  
   *Prefer the shortest predicate path that is likely to work; add expansions like `rdfs:subClassOf*` only when necessary.*
4. **Variable names**  
   *Use descriptive names (`?lipid`, `?enzyme`, …). You may use `?x` once as a generic placeholder.*
5. **Learn from previous failures**. Consult the error message in *Failed patterns* if one is provided.
6. **Look at examples** to understand how the schema looks like and what predicates/paths can be used. 

---

**Output format**

* Provide the generated SPARQL query inside a single markdown code block with the "sparql" language tag (````sparql ... ````).

* The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.

<example start>
PREFIX rh: <http://rdf.rhea-db.org/>

ASK WHERE {
  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea      rh:side/rh:contains/rh:compound ?compound .
    ?compound  (rh:chebi
              | rh:reactivePart/rh:chebi
              | rh:underlyingChebi/rh:chebi) ?metabolite .
  }
}
<example end>

**User question:** {{input}}

{{endpoint_description}}

**Example queries:** (natural question ↔ SPARQL pairs; may not be federated)  
{{extracted_example_queries}}

**Endpoint for this block (remote SERVICE endpoint):** {{service_endpoint}}

**Target endpoint** (primary execution endpoint): {{target_endpoint}}

**Mapping of entities identified in user question to ontology IRIs:** {{iri_mapping}}

**Failed patterns:** {{failed_pattern}}
"""
)






QUERY_ASSEMBLE_PROMPT  = (
    INTRODUCTION_PROMPT
    + """
    
**Task**
Your task is to merge validated building blocks into **one runnable federated query**.
The query needs to be created for the provided **target endpoint**.

Assemble a complete SPARQL query that:

1. **Runs on** the target endpoint: {{target_endpoint}}  
   This endpoint is the host; all other calls go inside `SERVICE {}` blocks.

2. **Federates with** the following remote endpoints:{{federated_endpoints}}

3. **Integrates** the **validated triple patterns** listed below, keeping their semantics intact but adjusting them as necessary (e.g., renaming variables, harmonizing prefixes) so they fit together into a single coherent query.

4. It might happen that for some endpoints none of the triple patterns/building blocks are working (indicated with <failed pattern>, <successful pattern>).**Learn from these previous failures** and orientate yourself on provided examples and context. 

5. **Identify** join variables between endpoints. 
  
6. Incorporats the *early draft* 'SELECT' variables. These have been used at an earlier stage as a 'north star' to serve as a rough orientation for the generation of the building blocks. It migh be necessary to change these or include additional variables. 

7. Include all **PREFIX** that are needed for the final query. 

**Output format**

* Provide the generated SPARQL query inside a single markdown code block with the "sparql" language tag (````sparql ... ````).

* The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.

**User question:** {{input}}

**Example queries:** (**Note:** These queries are examples of a natural questions with a corresponding sparql query. They may be not federated, but give hints about how the schema of an endpoint look like) 

{{extracted_example_queries}}

**Building blocks generated from the user question, examples and IRI mapping:** 

{{building_blocks}}

**Mapping of entities identified in user question to ontology IRIs:** 

{{iri_mapping}}

""")






QUERY_PATTERN_PROMPT_PRIMARY_BLOCK = (
    INTRODUCTION_PROMPT
    + """
**Task**

You are writing **the primary (local) block** of a federated SPARQL query.  
This block executes on the *primary* endpoint (`{{target_endpoint}}`), so **do not** wrap it in a `SERVICE` clause. Produce **exactly one** self‑contained snippet that:

* lists all necessary `PREFIX` declarations,
* places the triple pattern(s) directly inside the query body,
* is wrapped in `ASK WHERE { … }` so we can test it quickly.

The block alone will not fully answer the user’s question; its results will later be joined with remote blocks.

---
**Requirements**

1. **Exactly one block** – shape:  
   `PREFIX … ASK WHERE { … }`  (no `SERVICE` clause)
2. **Use the IRI bindings** in *Mapping* exactly (or IRIs from the examples); do not invent IRIs.
3. **Keep it minimal but meaningful**  
   *Choose the shortest predicate path likely to work; add limited expansions such as `rdfs:subClassOf*` only when essential.*
4. **Variable names**  
   *Use descriptive names (`?lipid`, `?enzyme`, …). You may use `?x` once for a generic placeholder.*
5. **Learn from previous failures**. Consult the error message in *Failed pattern* if one is provided. 
6. **Look at examples** to understand how the schema looks like and what predicates/paths can be used.

---
**Output format**

* Provide the generated SPARQL query inside a single markdown code block with the "sparql" language tag (````sparql ... ````).

* The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.

<example start>
PREFIX rh: <http://rdf.rhea-db.org/>

ASK WHERE {
  ?rhea      rh:side/rh:contains/rh:compound ?compound .
  ?compound  (rh:chebi
            | rh:reactivePart/rh:chebi
            | rh:underlyingChebi/rh:chebi) ?metabolite .
}
<example end>

**User question:** {{input}}

{{endpoint_description}}

**Example queries:** (natural‑language question ↔ SPARQL answer pairs; may not be federated)  
{{extracted_example_queries}}

**Target endpoint** (primary execution endpoint): {{target_endpoint}}

**Mapping of entities identified in user question to ontology IRIs:** {{iri_mapping}}

**Failed patterns:** {{failed_pattern}}
"""
)