from .general import INTRODUCTION_PROMPT




CONSTRUCTION_PROMPT_AUGMENTED = (
    INTRODUCTION_PROMPT
    + """
Potential entities extracted from the user question {{potential_entities}}

Potential classes extracted from the user question  {{potential_classes}}

Example  queries (**Note:** These queries are examples of a natural questions with a corresponding sparql query. They may be not federated, but give hints about how the schema of an endpoint look like) {{extracted_example_queries}}

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
Generate a **federated SPARQL query** to answer the user question, utilising the provided inputs (question, classes, entities, endpoints).

**Requirements:**

1.**Answer Question:** The query must aim to retrieve information that directly answers the user's question.

2.**Federated:** The query **must** use `SERVICE <endpoint_uri>  ...` clauses to query the relevant endpoints from the provided context list as needed.

3.**Prefixes:** For better readability, the query **should** contain prefixes.

4.**Computational Efficiency:** As a guideline, aim for computational efficiency by keeping the query structure as simple and direct as possible to answer the question.

5.**Comments:** Provide comments in the query to explain the logic behind the construction and any assumptions made during the generation process.

6.**Output Format:** Provide the generated SPARQL query inside a single markdown code block with the "sparql" language tag (````sparql ... ````).

7. **Endpoint Comment:** - The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.
                                                                                                 
                         - Include only this single primary endpoint URL comment at the start. No other text on this line or preceding it within the code block.

8. **Context Adherence:** - Always derive your answer from focusing on endpoint URLs and schema information provided in the input context. Do not try to create a query from nothing and do not provide a generic query.

                          - Due to the nature of federated sparql queries it might be that some are not included in the input context. In this case reason about for which endpoints (databases) it would make sense to federate with.
                                                  
"""
)