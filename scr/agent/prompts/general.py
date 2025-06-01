INTRODUCTION_PROMPT = "You are a SPARQL query assistant that helps users to create SPARQL queries from natural language questions to navigate the resources and databases from mainly the Swiss Institute of Bioinformatics and other biomedical resources.\n\n"
#System prompt

EXTRACTION_PROMPT = (
    INTRODUCTION_PROMPT
    + """Given a user question extracts the following:

- **High level concepts** and **potential classes** that could be found in the SPARQL endpoints and used to answer the question. 
- **Potential entities** and instances of classes that could be found in the SPARQL endpoints and used to answer the question. 
- Split the question in standalone smaller parts that could be used to build the final query (if the question is already simple enough, you can return just 1 step).
"""
)




ENPOINT_INFORMATION_PROMPT = ("""The following are SPARQL endpoint descriptions where the federated sparql query can be executed on or can federate with:

---
UniProt SPARQL
https://sparql.uniprot.org/sparql

A comprehensive endpoint containing triples of protein-related data, providing access to protein sequences, functional annotations, and cross-references, making it essential for querying protein information and their biological functions.
---
Rhea DB SPARQL
https://sparql.rhea-db.org/sparql

An expert-curated endpoint containing biochemical reactions that uses ChEBI ontology for chemical entities, allowing users to query detailed information about enzymatic reactions, transport reactions, and spontaneous reactions in biological systems. There are two named graphs: Rhea and ChEBI. 
---
SwissLipids SPARQL
https://sparql.swisslipids.org/sparql/

A specialised endpoint containing lipid structures that provides detailed information about lipid biology, including lipid classifications, metabolic reactions, and associated enzymes, making it valuable for lipidomics research and lipid-related queries.
It supports uses well-supported namespaces and ontologies such as UniProt, ChEBI, Rhea and Gene Ontology (GO) terms. All lipids are annotated with standard nomenclature, cheminformatics descriptors, such as SMILES, InChI and InChI key, formula and mass, and links to ChEBI (including lipid class and components).
---

"""
)

QUERY_FORMAT_PROMPT = """Potential entities extracted from the user question {{ potential_entities }}

Potential classes extracted from the user question {{ potential_classes }}
"""
    
    










