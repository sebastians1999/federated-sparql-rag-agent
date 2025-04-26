examples_few_shot_federated_query_generation = [
  {
  "user": "Human question: For a given lipid (SWISSLIPID:000399814, Ceramide), return a list of all corresponding reactions (Rhea IDs and equation).",

  "context": 
      """Potential entities extracted from the user question [{'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1816978', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7762046456336975, 'endpoint_url': ''}, page_content='Eois nr. trillista EOISD030-14'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/472974', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.774516224861145, 'endpoint_url': ''}, page_content='Nephila cf. pilipes FAPMCZ05'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2548452', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7744662165641785, 'endpoint_url': ''}, page_content='Eurotiales sp. IK_Pi14'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1816941', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7655302882194519, 'endpoint_url': ''}, page_content='Eois nr. lucivittata BOLD:ABW9062'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2990340', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7652775645256042, 'endpoint_url': ''}, page_content='Parupeneus sp. S0014_018')], 'text': 'SWISSLIPID:000399814'}, {'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_17761', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 1.0, 'endpoint_url': ''}, page_content='ceramide'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_71986', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8857792615890503, 'endpoint_url': ''}, page_content='C20 ceramide'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_84404', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8758777379989624, 'endpoint_url': ''}, page_content='ceramide 1-phosphate(2-)'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/31380', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.8507953882217407, 'endpoint_url': ''}, page_content='Ceramium'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2802', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.8414799571037292, 'endpoint_url': ''}, page_content='Ceramiales')], 'text': 'Ceramide'}]

Potential classes extracted from te user question  [{'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16708', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7592589855194092, 'endpoint_url': ''}, page_content='adenine'), Document(metadata={'uri': 'http://rdf.rhea-db.org/56996', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7422156929969788, 'endpoint_url': ''}, page_content='aldehydo-D-apiose = apulose'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16040', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7418680787086487, 'endpoint_url': ''}, page_content='cytosine'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_1230', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7398353815078735, 'endpoint_url': ''}, page_content='sophorose'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16651', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7370398044586182, 'endpoint_url': ''}, page_content='(S)-lactate')], 'text': 'Enzyme'}, {'matchs': [Document(metadata={'uri': 'http://rdf.rhea-db.org/45248', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7081648111343384, 'endpoint_url': ''}, page_content='butanoate(out) = butanoate(in)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_31334', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.706755518913269, 'endpoint_url': ''}, page_content='(E)-caffeyl alcohol'), Document(metadata={'uri': 'http://rdf.rhea-db.org/79099', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7015789151191711, 'endpoint_url': ''}, page_content='cholate + L-histidine = L-histidocholate + H2O'), Document(metadata={'uri': 'http://rdf.rhea-db.org/27958', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7013691663742065, 'endpoint_url': ''}, page_content='cytidine + H2O = cytosine + D-ribose'), Document(metadata={'uri': 'http://rdf.rhea-db.org/34983', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7012451887130737, 'endpoint_url': ''}, page_content='sulfate(in) = sulfate(out)')], 'text': 'Reaction'}, {'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_57957', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8491368293762207, 'endpoint_url': ''}, page_content='lipid X(2-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_60033', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8478032350540161, 'endpoint_url': ''}, page_content='lipid II(3-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_58712', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8394752144813538, 'endpoint_url': ''}, page_content='lipid A(4-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16113', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8225206732749939, 'endpoint_url': ''}, page_content='cholesterol'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_193141', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8218621015548706, 'endpoint_url': ''}, page_content='a lipid A(4-)')], 'text': 'Lipid'}]
""",

  "endpoint_information": """The following are SPARQL endpoint descriptions where the federated sparql query can be executed on or can federate with:

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
""",

"output": 
  """## Step 1 – Identify main entities / classes  
**Reasoning**  
From the natural language question the primary thing we must start with is **Ceramide**, which is explicitly given by its SwissLipids identifier `SWISSLIPID:000399814`. 
The user would like to retrieve the corresponing reactions to this Lipid and already refers to a specific endpoint/namespace. 
Thus the expected output are reactions and from the Rhea endpoint. 
So:  
- **Seed entity** `SWISSLIPID:000399814` (a class of lipids)  
- **Target class** Rhea reactions

---

## Step 2 – Determine return labels (future `SELECT` vars)  
**Reasoning**  
The user wants:
1. The original lipid & its name (so they see context).  
2. Any descendant/related lipid ids & names(Ceramide is a class of lipids). 
3. The ChEBI cross‑ref that bridges lipids to reactions.  
4. Every matching reaction id **and** its full equation text.  
Chosen variables (names suggest meaning):  
`?startId ?startName ?id ?name ?chebi ?rhea ?rheaEquation`       

---

## Step 3 – Map entities to ontology IRIs (If there is not a good match in the provided context figure out a mapping from your knowledge)
**Reasoning**  
We already know the textual ID `SWISSLIPID:000399814` given from the question. 
In the Rhea endpoint **rhea reactions** are defined as rh:Reaction.

---

## Step 4 – Locate SPARQL endpoints and what information we seek to retrieve from that endpoint.
**Reasoning**  
- *SwissLipids* hosts its own public endpoint (context tells us). Since we we are seeking to retrieve information for the SWISSLIPID:000399814 (Ceramide lipid class), we need to know what lipids are in that class. From the context we know that SwissLipids provides detailed information about lipid classification. Thus this endpoint will serve us to retrieve which lipids belong to the Ceramide lipid class. 
  
- *Rhea* (the user already indicated in the question to use this endpoint). In the question the user asked to find all reactions that correspond to SWISSLIPID:000399814 (Ceramide lipid class). From the conext we know that Rhea is an edpoint containing biochemical reactions. Thus this edpoint will provide us with information about reactions, which is what the user asked for. 

**endpoints**:
- https://sparql.swisslipids.org/sparql/
- https://sparql.rhea-db.org/sparql

We therefore need a **federated query** with one SERVICE SERVICE <endpoint_uri>  ...` clause.

---

## Step 5 – Choose the primary endpoint  
**Reasoning** 

 To identify the relevant reactions, we first need to determine which lipids (including subclasses of Ceramide) we are working with. This means the SwissLipids dataset should drive the query, as it provides the starting point for what the user is asking for and the lipid hierarchy. The Rhea dataset is secondary and will only be queried to retrieve reactions for the lipids identified in SwissLipids.

---

## Step 6 – Identify join variables between endpoints   
**Reasoning**  
After examining the endpoint descriptions, we noted that both SwissLipids ("links to ChEBI") and Rhea ("uses ChEBI ontology") explicitly mention using ChEBI identifiers for chemical entities.
This common reference strongly suggests we can use ChEBI as the bridge to link information between the two databases.

- SwissLipids maps its lipid identifiers (?id) to corresponding ChEBI identifiers (using owl:equivalentClass ?chebi).
- Rhea uses these same ChEBI identifiers (?chebi) to specify the chemical compounds involved in its reactions (via rh:chebi).

Therefore, the ChEBI identifier, stored in the variable ?chebi, serves as the crucial join variable connecting the two datasets within the federated query.

---

## Step 7 – Draft triple patterns in each endpoint 
**Reasoning**
The relevant Rhea predicates for equations and for linking to a ChEBI compound (found by reading Rhea’s ontology) are:  
- `rh:equation` (gives the human‑readable equation)  
- path `rh:side/rh:contains/rh:compound/rh:chebi` (pulls the ChEBI id in each reaction side)
- to retrieve the instances in the SWISSLIPID:000399814 (Ceramide lipid class) we can make use of the subClassOf* property which is part of the rdfs namespace. 

### 7 a. SwissLipids graph 

```sparql
VALUES ?startId { SWISSLIPID:000399814 }   # seed
?startId rdfs:label ?startName .
?id      rdfs:subClassOf* ?startId .       # include subclasses / lipids
?id      rdfs:label        ?name .
?id      owl:equivalentClass ?chebi .      # chebi bridging
```
### 7 b. Rhea graph 

```sparql
?rhea rh:equation ?rheaEquation .
?rhea rh:side/rh:contains/rh:compound/rh:chebi ?chebi .
```

---

## Step 8 – Mark federated patterns with `SERVICE`  
**Reasoning**  
Wrap the triple patterns of the endpoints the primary enpoint federates with inside SERVICE clauses.
We use the Rhea URI we determined in step 4 for the SERVICE block and put it between <URI>. 
  
```sparql
SERVICE <https://sparql.rhea-db.org/sparql> { … }
```
---

## Step 9 – Assemble the `WHERE` block
**Reasoning**
Combine the patterns from Step 7, incorporating the SERVICE block from Step 8 correctly within the OPTIONAL structure.  

```sparql
WHERE {
  VALUES ?startId { SWISSLIPID:000399814 }
  ?startId rdfs:label ?startName .
  ?id rdfs:subClassOf* ?startId .
  ?id rdfs:label ?name .
  ?id owl:equivalentClass ?chebi .

  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:equation ?rheaEquation .
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi ?chebi .
  }
}
```

---

## Step 10 – Filtering / extras  
**Reasoning**
Nothing extra needed; but a simple ordering improves readability.

```sparql
WHERE {
  VALUES ?startId { SWISSLIPID:000399814 }
  ?startId rdfs:label ?startName .
  ?id rdfs:subClassOf* ?startId .
  ?id rdfs:label ?name .
  ?id owl:equivalentClass ?chebi .

  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:equation ?rheaEquation .
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi ?chebi .
  }
}
ORDER BY ?startId ?id
```

---

## Step 11 – Write the `SELECT` clause with the variables we determined in step 2.

```sparql
SELECT ?startId ?startName ?id ?name ?chebi ?rhea ?rheaEquation
WHERE {
  VALUES ?startId { SWISSLIPID:000399814 }
  ?startId rdfs:label ?startName .
  ?id rdfs:subClassOf* ?startId .
  ?id rdfs:label ?name .
  ?id owl:equivalentClass ?chebi .

  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:equation ?rheaEquation .
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi ?chebi .
  }
}
ORDER BY ?startId ?id
```

---

## Step 12 – Namespace prefixes and target endpoint. 
 **Reasoning**
Define the prefixes. For the target endpoint (rh) use the the URI we identified in step 4.
The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint which we determined in step 5. 

```sparql
#https://sparql.swisslipids.org/sparql/
PREFIX SWISSLIPID: <https://swisslipids.org/rdf/SLM_>
PREFIX owl:        <http://www.w3.org/2002/07/owl#>
PREFIX rdfs:       <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rh:         <http://rdf.rhea-db.org/>

SELECT ?startId ?startName ?id ?name ?chebi ?rhea ?rheaEquation
WHERE {
  VALUES ?startId { SWISSLIPID:000399814 }
  ?startId rdfs:label ?startName .
  ?id rdfs:subClassOf* ?startId .
  ?id rdfs:label ?name .
  ?id owl:equivalentClass ?chebi .

  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:equation ?rheaEquation .
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi ?chebi .
  }
}
ORDER BY ?startId ?id
```"""
},
{
  "user": "Human question: Select all approved reactions with CHEBI:17815 (a 1,2-diacyl-sn-glycerol) or one of its descendant. Display links to UniProtKB/Swiss-Prot entries via EC numbers if the link rhea-ec exists.",

  "context": 
      """Potential entities extracted from the user question [{'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1355255', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7805784344673157, 'endpoint_url': ''}, page_content='Bacillus sp. 17815'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2569175', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7691332101821899, 'endpoint_url': ''}, page_content='Charca nr. triquetra Pe_Geo_3045'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2068199', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7653384208679199, 'endpoint_url': ''}, page_content='Eois nr. hocica 48215'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1037303', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7584422826766968, 'endpoint_url': ''}, page_content='Eteone aff. longa CMC05'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1491101', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.752835750579834, 'endpoint_url': ''}, page_content='Diaporthe cf. heveae C25')], 'text': 'CHEBI:17815'}, {'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_17815', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.9999998211860657, 'endpoint_url': ''}, page_content='1,2-diacyl-sn-glycerol'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_75524', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.9702757000923157, 'endpoint_url': ''}, page_content='2,3-diacyl-sn-glycerol'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_77272', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.9587045907974243, 'endpoint_url': ''}, page_content='1,3-diacyl-sn-glycerol'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_76585', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.9508001804351807, 'endpoint_url': ''}, page_content='1-alkyl-2,3-diacyl-sn-glycerol'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_145394', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.946038544178009, 'endpoint_url': ''}, page_content='1,2-diacyl-sn-glycero-3-phosphoglycerol(1-)')], 'text': '1,2-diacyl-sn-glycerol'}, {'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2632911', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7738710641860962, 'endpoint_url': ''}, page_content='unclassified Archips'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2685085', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7506400346755981, 'endpoint_url': ''}, page_content='unclassified Proterops'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2787823', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7477089166641235, 'endpoint_url': ''}, page_content='unclassified entries'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2632054', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7403478622436523, 'endpoint_url': ''}, page_content='unclassified Repipta'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2622348', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7399873733520508, 'endpoint_url': ''}, page_content='unclassified Stripsipher')], 'text': 'UniProtKB/Swiss-Prot entries'}, {'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/338641', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7255591154098511, 'endpoint_url': ''}, page_content='nr. Ecclisister sp. MSC-2005'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_131969', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7212393283843994, 'endpoint_url': ''}, page_content='(11S,12R)-EET(1-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_131970', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7201716899871826, 'endpoint_url': ''}, page_content='(11R,12S)-EET(1-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_76625', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.711582601070404, 'endpoint_url': ''}, page_content='11,12-EET(1-)'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/1082751', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7085391879081726, 'endpoint_url': ''}, page_content='Sordariales sp. ECM150')], 'text': 'EC numbers'}]

Potential classes extracted from te user question  [{'matchs': [Document(metadata={'uri': 'http://rdf.rhea-db.org/45248', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7081648111343384, 'endpoint_url': ''}, page_content='butanoate(out) = butanoate(in)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_31334', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.706755518913269, 'endpoint_url': ''}, page_content='(E)-caffeyl alcohol'), Document(metadata={'uri': 'http://rdf.rhea-db.org/79099', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7015789151191711, 'endpoint_url': ''}, page_content='cholate + L-histidine = L-histidocholate + H2O'), Document(metadata={'uri': 'http://rdf.rhea-db.org/27958', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7013691663742065, 'endpoint_url': ''}, page_content='cytidine + H2O = cytosine + D-ribose'), Document(metadata={'uri': 'http://rdf.rhea-db.org/34983', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7012451887130737, 'endpoint_url': ''}, page_content='sulfate(in) = sulfate(out)')], 'text': 'reaction'}]
  """,
  "endpoint_information": """The following are SPARQL endpoint descriptions where the federated sparql query can be executed on or can federate with:

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
""",
  "output": """
  ## Step 1 – Identify main entities / classes
**Reasoning**
The core of the question revolves around finding **reactions** associated with a specific chemical entity, **CHEBI:17815** (1,2-diacyl-sn-glycerol), and its descendants. The user specifies constraints: only **approved** reactions are wanted. Additionally, there's a conditional requirement to link these reactions to **UniProtKB/Swiss-Prot entries** via **EC numbers**.
So:
- **Seed entity:** `CHEBI:17815` (a specific chemical class)
- **Target class:** Rhea reactions


---

## Step 2 – Determine return labels (future `SELECT` vars)
**Reasoning**
The user wants:
1.  The **reactions** that match the criteria.
2.  The associated **enzyme** (EC number) if the link exists.
3.  The user did not specifically asked for it, but a count of distinct **UniProtKB/Swiss-Prot entries** linked to that enzyme will probably enrich the information the user is asking for.

Chosen variables (based on the ground truth query):
`?reaction ?enzyme ?proteinCount`

---

## Step 3 – Map entities to ontology IRIs
**Reasoning**

In the question the user already provided an entity identifier for 1,2-diacyl-sn-glycerol (a chemical class), which is CHEBI:17815. 
In Rhea, reactions are instances or subclasses of `rh:Reaction`. We can an make use of the subClassOf* property which is part of the rdfs namespace to retrieve the reactions. 
Rhea also uses the object `rh:Approved` with the property `rh:status`.
Furthermore Rhea links reactions to EC numbers via `rh:ec`. UniProt links proteins to EC numbers (enzymes) via `up:enzyme`.
Links to UniProtKB/Swiss-Prot entries are are identified in UniProt by having `up:reviewed true`.

---

## Step 4 – Locate SPARQL endpoints and what information we seek to retrieve from that endpoint.
**Reasoning**

-   **Rhea** From the conext we know that Rhea is an edpoint containing biochemical reactions. Since the user is asking for **reactions** this endpoint is needed to find reactions (`?reaction`). Since Rhea uses ChEBI ontology for chemical entities, based on the participant ChEBI entity (`?chebi`), we can check their status (`rh:Approved`), and find associated EC numbers (`rh:ec`). This is the primary source for reaction data.

-   **UniProt** This endpoint is required *conditionally* (as indicated by "if the link... exists") to find reviewed UniProt entries (`?protein`) linked to the EC numbers (`?enzyme`) obtained from Rhea. This provides the connection to Swiss-Prot entries.

**Endpoints**:
-   https://sparql.rhea-db.org/sparql 
-   https://sparql.uniprot.org/sparql 

We therefore need a **federated query** with one SERVICE SERVICE <endpoint_uri>  ...` clause..

---

## Step 5 – Choose the primary endpoint
**Reasoning**
The query starts by searching for reactions based on a chemical entity (CHEBI:17815) and its status. This information resides in the Rhea database. The UniProt information is supplementary (as indicated in our previous step it is only **conditionally**) and dependent on finding an EC number in Rhea first. Therefore, Rhea is the primary endpoint.

---

## Step 6 – Identify join variables between endpoints
**Reasoning**
The link between Rhea and UniProt is the **EC number**.
-   In Rhea, the reaction `?reaction` is linked to an EC number via the property `rh:ec`. We'll capture this in the variable `?enzyme`.
-   In UniProt, reviewed proteins `?protein` are linked to an EC number via the property `up:enzyme`. We'll use the same variable `?enzyme` for the join.

---

## Step 7 – Draft triple patterns in each endpoint
**Reasoning**
As decided in Step 5, Rhea is our primary endpoint. To find the target reactions, we use the class rh:Reaction identified in Step 3: ?reaction rdfs:subClassOf rh:Reaction .. We apply the constraint for approved reactions, also identified in Step 3, using ?reaction rh:status rh:Approved .. To connect these reactions to the seed chemical entity CHEBI:17815 and its descendants (a requirement from Step 1), we follow the path through reaction sides (rh:side), participants (rh:contains, rh:participant), and compounds (rh:compound) to the ChEBI identifier (?chebi), as established in Step 3. The inclusion of descendants is handled using the property path ?chebi rdfs:subClassOf* CHEBI:17815 ., again based on the mapping in Step 3. For the conditional link to UniProt specified in Steps 1 and 4, we need the EC number, which Rhea links via rh:ec (Step 3). In the federated UniProt endpoint, we use the patterns ?protein up:reviewed true . and ?protein up:enzyme ?enzyme . to find the reviewed proteins linked via the EC number (?enzyme), which was identified as the join variable in Step 6. These UniProt patterns, along with the retrieval of ?enzyme using rh:ec, will be placed within an OPTIONAL block containing the SERVICE call, reflecting the conditional nature established in Step 4.


### 7a. Rhea graph 

```sparql
# Find reactions and check status
?reaction rdfs:subClassOf rh:Reaction .
?reaction rh:status rh:Approved .

# Link reaction to participants and ChEBI entity (including descendants)
?reaction rh:side ?reactionSide .
?reactionSide rh:contains ?participant .
?participant rh:compound ?compound .
?compound rh:chebi ?chebi .
?chebi rdfs:subClassOf* CHEBI:17815 . # Match CHEBI:17815 or descendants

# Optionally get the EC number
OPTIONAL { ?reaction rh:ec ?enzyme . }
```
### 7b. UniProt graph (Federated, inside OPTIONAL)

```sparql
# Find reviewed proteins associated with the enzyme (EC number)
?protein up:reviewed true .
?protein up:enzyme ?enzyme .
Note: This part only executes if ?enzyme was bound in the Rhea part. We'll wrap the entire UniProt query within the main OPTIONAL block that finds ?enzyme, and potentially move the rh:ec pattern inside the optional block too, as per the ground truth structure.
```

---

Step 8 – Mark federated patterns with SERVICE
**Reasoning**
The UniProt patterns need to be enclosed in a SERVICE block within the query structure. Since the UniProt lookup depends on finding an ?enzyme (EC number) in Rhea, and the user only wants the link if it exists, the entire SERVICE call should be within an OPTIONAL block, which itself depends on ?reaction rh:ec ?enzyme.
We use the Rhea URI we determined in step 4 for the SERVICE block and put it between <URI>. 

```sparql
OPTIONAL {
  ?reaction rh:ec ?enzyme .
  SERVICE <https://sparql.uniprot.org/sparql> {
    ?protein up:reviewed true .
    ?protein up:enzyme ?enzyme.
  }
}
```

--- 

Step 9 – Assemble the WHERE block
**Reasoning**
Combine the patterns from Step 7, incorporating the SERVICE block from Step 8 correctly within the OPTIONAL structure.

```sparql
WHERE {
  # Core Rhea patterns
  ?reaction rdfs:subClassOf rh:Reaction .
  ?reaction rh:status rh:Approved .
  ?reaction rh:side ?reactionSide .
  ?reactionSide rh:contains ?participant .
  ?participant rh:compound ?compound .
  ?compound rh:chebi ?chebi .
  ?chebi rdfs:subClassOf* CHEBI:17815 .

  # Optional block for EC number and UniProt federation
  OPTIONAL {
    ?reaction rh:ec ?enzyme .
    SERVICE [https://sparql.uniprot.org/sparql](https://sparql.uniprot.org/sparql) {
      ?protein up:reviewed true .
      ?protein up:enzyme ?enzyme.
    }
  } . # to include the OPTIONAL block properly we need to set a '.' here. 
}
```

---

## Step 10 – Filtering / extras
**Reasoning**

As determined in step two the user did not explicitly ask for count but it may enrich the information the user has asked for. Thus we include the aggregation COUNT. 
To only count the number of distinct proteins per reaction/enzyme pair we also include GROUP BY. By simple ordering (ORDER BY) we improve readabilty for the user. 

```sparql
WHERE {
  # (Same patterns as Step 9)
  ?reaction rdfs:subClassOf rh:Reaction .
  ?reaction rh:status rh:Approved .
  ?reaction rh:side ?reactionSide .
  ?reactionSide rh:contains ?participant .
  ?participant rh:compound ?compound .
  ?compound rh:chebi ?chebi .
  ?chebi rdfs:subClassOf* CHEBI:17815 .

  OPTIONAL {
    ?reaction rh:ec ?enzyme .
    SERVICE [https://sparql.uniprot.org/sparql](https://sparql.uniprot.org/sparql) {
      ?protein up:reviewed true .
      ?protein up:enzyme ?enzyme.
    }
  } .
}
GROUP BY ?reaction ?enzyme
ORDER BY ?reaction
```

---

## Step 11 – Write the SELECT clause with the variables we determined in step 2.
**Reasoning**
Since a protein can be related to more than one reaction we need to make sure that we only retrieve distinct ?reaction and ?enzyme. 

```sparql
SELECT distinct ?reaction ?enzyme (count(distinct ?protein) as ?proteinCount)
WHERE {
  ?reaction rdfs:subClassOf rh:Reaction .
  ?reaction rh:status rh:Approved .
  ?reaction rh:side ?reactionSide .
  ?reactionSide rh:contains ?participant .
  ?participant rh:compound ?compound .
  ?compound rh:chebi ?chebi .
  ?chebi rdfs:subClassOf* CHEBI:17815 .

  OPTIONAL {
    ?reaction rh:ec ?enzyme .
    SERVICE [https://sparql.uniprot.org/sparql](https://sparql.uniprot.org/sparql) {
      ?protein up:reviewed true .
      ?protein up:enzyme ?enzyme.
    }
  } . 
}
GROUP BY ?reaction ?enzyme
ORDER BY ?reaction
```

---
### Step 12 – Namespace prefixes
**Reasoning**
Define the prefixes. For the target endpoint (rh) use the the URI we identified in step 4.
The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.

```sparql
#https://sparql.rhea-db.org/sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rh:<http://rdf.rhea-db.org/>
PREFIX CHEBI:<http://purl.obolibrary.org/obo/CHEBI_>
PREFIX up:<http://purl.uniprot.org/core/>

SELECT distinct ?reaction ?enzyme (count(distinct ?protein) as ?proteinCount)
WHERE {
  ?reaction rdfs:subClassOf rh:Reaction .
  ?reaction rh:status rh:Approved .
  ?reaction rh:side ?reactionSide .

  OPTIONAL {
    ?reaction rh:ec ?enzyme .
    SERVICE <https://sparql.uniprot.org/sparql> {
      ?protein up:reviewed true .
      ?protein up:enzyme ?enzyme.
    }
  } .

  ?reactionSide rh:contains ?participant .
  ?participant rh:compound ?compound .
  ?compound rh:chebi ?chebi .
  ?chebi rdfs:subClassOf* CHEBI:17815 .
}
GROUP BY ?reaction ?enzyme
ORDER BY ?reaction
```
  """
},
{
    "user": "Human question: Retrieve human enzymes that metabolize sphingolipids and are annotated in ChEMBL.",

    "context": 
      """Potential entities extracted from the user question: [{'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/9605', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.807994544506073, 'endpoint_url': ''}, page_content='Homo'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/2904496', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.743664026260376, 'endpoint_url': ''}, page_content='Alex'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/9606', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7413591146469116, 'endpoint_url': ''}, page_content='Homo sapiens'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/3135724', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7277826070785522, 'endpoint_url': ''}, page_content='Arthroplea congener'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/245576', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7268465757369995, 'endpoint_url': ''}, page_content='Conoplea')], 'text': 'human'}, {'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_64583', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8562774658203125, 'endpoint_url': ''}, page_content='sphingoid 1-phosphate(1-)'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_26739', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.98208152055740356, 'endpoint_url': ''}, page_content='sphingolipids'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_60119', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.8160674571990967, 'endpoint_url': ''}, page_content='sphingosine 1-phosphate(1-)'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/84566', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.8143690824508667, 'endpoint_url': ''}, page_content='Sphingobacteriaceae'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/26739', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.8141623139381409, 'endpoint_url': ''}, page_content='Sphinga')], 'text': 'sphingolipids'}, {'matchs': [Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/87969', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7675694823265076, 'endpoint_url': ''}, page_content='Cymbula'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/543400', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7574917078018188, 'endpoint_url': ''}, page_content='Cymbium'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/270290', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7417998313903809, 'endpoint_url': ''}, page_content='Symbiodinium sp. C3L'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/927627', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.7401735186576843, 'endpoint_url': ''}, page_content='Cymbium cymbium'), Document(metadata={'uri': 'http://purl.uniprot.org/taxonomy/14366', 'type': 'literal', 'description': 'taxon scientific names', 'score': 0.732369065284729, 'endpoint_url': ''}, page_content='Cymbidium')], 'text': 'ChEMBL'}]

Potential classes extracted from the user question: [{'matchs': [Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16708', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7592589855194092, 'endpoint_url': ''}, page_content='adenine'), Document(metadata={'uri': 'http://rdf.rhea-db.org/56996', 'type': 'literal', 'description': 'Reactions in RHEA.', 'score': 0.7422156929969788, 'endpoint_url': ''}, page_content='aldehydo-D-apiose = apulose'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16040', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7418680787086487, 'endpoint_url': ''}, page_content='cytosine'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_1230', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7398353815078735, 'endpoint_url': ''}, page_content='sophorose'), Document(metadata={'uri': 'http://purl.obolibrary.org/obo/CHEBI_16651', 'type': 'literal', 'description': 'Chemical entities in ChEBI.', 'score': 0.7370398044586182, 'endpoint_url': ''}, page_content='(S)-lactate')], 'text': 'enzyme'}]
  """,

    "endpoint_information": """The following are SPARQL endpoint descriptions where the federated sparql query can be executed on or can federate with:

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
""",

    "output": 
      """## Step 1 – Identify main entities / classes
**Reasoning**
The question asks for **enzymes** (proteins with catalytic activity) specifically from **human** that **metabolize** (are involved in reactions with) **sphingolipids** and have an **annotation in ChEMBL**.
- **Seed entities:** `human` (organism), `sphingolipids` (metabolite class), `ChEMBL` (database reference).
- **Target class:** `enzyme` (proteins).
- **Relationships:** `metabolize` (connecting enzymes to sphingolipids via reactions), `annotated in` (connecting enzymes to ChEMBL database links).

---

## Step 2 – Determine return labels (future `SELECT` vars)
**Reasoning**
The user wants a list of:
1.  The human enzymes (identified by their protein URI).
2.  Their corresponding ChEMBL annotations (identified by the ChEMBL entry URI).
Chosen variables (names suggest meaning):
`?protein ?chemblEntry`

---

## Step 3 – Map entities to ontology IRIs (If there is not a good match in the provided context figure out a mapping from your knowledge)
**Reasoning**
- **human:** In the context under potential entities we can map *human* to the label *Homo Sapiens*, which has the taxonomy identifier`http://purl.uniprot.org/taxonomy/9606`. We use the prefix `taxon:9606`.
- **sphingolipids:** This is a broad class. The potential entities from the context include `CHEBI:64583` (sphingosine 1-phosphate(1-)) and `CHEBI:26739` (sphingolipids). Sphingolipids is exactly what we are looking for, and it also has a high retrieval similarity score.
- **enzyme:** In UniProt, these are `up:Protein` resources that have an associated `up:CatalyticActivity`.
- **annotated in ChEMBL:** This refers to a cross-reference link from UniProt. The link target (`?chemblEntry`) must have a `up:database` property pointing to the specific IRI for the ChEMBL database: `<http://purl.uniprot.org/database/ChEMBL>`.

---

## Step 4 – Locate SPARQL endpoints and what information we seek to retrieve from that endpoint.
**Reasoning**

- **UniProt:**From the description we know that UniProt is a database containing information about protein-related data. The user is asking about **enzymes**. Most enzymes are proteins. Thus, we can use UniProt to retrieve information about these specific enzymes the user is asking for. Since we are seeking human enzymes, we can also use UniProt to filter by organism (taxon:9606).
To precisely identify relevant proteins with enzymatic functions, we focus on proteins that exhibit catalytic activity (up:CatalyticActivity). This property allows us to narrow down the dataset to proteins that act as enzymes.

- **Rhea:** Rhea needs to identify reactions that involve the target lipid class (`CHEBI:26739` or subclasses). 

**endpoints**:
- https://sparql.uniprot.org/sparql
- https://sparql.rhea-db.org/sparql

A **federated query** is required to combine information from UniProt (proteins, organism, annotations) and Rhea (reactions involving specific lipids).

---

## Step 5 – Choose the primary endpoint
**Reasoning**
The core of the query is finding *proteins* associated with a specific *organism* and having specific *database annotations* (ChEMBL). This information resides primarily in UniProt. Rhea serves as a filter, providing the set of relevant *reactions* that these proteins must catalyze. Therefore, UniProt is the primary endpoint, and we will query Rhea using a `SERVICE` clause within the UniProt query.

---

## Step 6 – Identify join variables between endpoints
**Reasoning**

We seek to identifiy 

We already identified in previous steps that we can use Rhea as a filter providing the set of relevant *reactions* that are part of the sphingolipids class. So Rhea filters on these reactions and only retrieves the ones that are relevant for us (class of sphingolipids).
Therefore, `?rhea` is the variable that connects the information retrieved from UniProt (which enzyme catalyzes which reaction) with the information retrieved from Rhea (which reactions involve sphingolipids).

---

## Step 7 – Draft triple patterns in each endpoint
**Reasoning**
For Rhea we aim to find reaction IRIs (`?rhea`) where at least one participant is `CHEBI:26739` or a subclass thereof.
Relevant predicates: `rh:side/rh:contains/rh:compound/rh:chebi` (path to participant ChEBI ID), `rdfs:subClassOf` (property path for class hierarchy).
Looking at Uniprot we need to find human proteins (?protein) that catalyze a reaction (?rhea obtained from Rhea) and have a ChEMBL cross-reference (?chemblEntry).
Relevant predicates are: up:organism, up:annotation, up:catalyticActivity, up:catalyzedReaction, rdfs:seeAlso, up:database.

### 7a. Rhea graph
```sparql
?hea rdfs:subClassOf rh:Reaction; # we first filter for reactions #rhea bridging
rh:side/rh:contains/rh:compound/rh:chebi rdfs:subClassOf+ CHEBI:26739 .
```
### 7b. UniProt graph 
?ca up:catalyzedReaction ?rhea . # rhea bridging
?protein up:annotation/up:catalyticActivity ?ca .

# Filter for human organism
?protein up:organism taxon:9606 .

# Filter for ChEMBL annotation
?protein rdfs:seeAlso ?chemblEntry .
?chemblEntry up:database <http://purl.uniprot.org/database/ChEMBL> .
```

---

Step 8 – Mark federated patterns with SERVICE
**Reasoning**  
Wrap the triple patterns of the endpoints the primary enpoint federates with inside SERVICE clauses:   

```sparql
SERVICE <https://sparql.rhea-db.org/sparql> {
  ?rhea rh:side/rh:contains/rh:compound/rh:chebi rdfs:subClassOf+ CHEBI:26739 .
}
```

---

Step 9 – Assemble the WHERE block

```sparql
WHERE {
  # 1. Find relevant reactions in Rhea
  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi rdfs:subClassOf+ CHEBI:26739 .
  }
  # 2. Find human proteins in UniProt that catalyze these reactions
  ?protein up:annotation/up:catalyticActivity ?ca .
  ?ca up:catalyzedReaction ?rhea .
  ?protein up:organism taxon:9606 .
  # 3. Ensure these proteins have a ChEMBL annotation
  ?protein rdfs:seeAlso ?chemblEntry .
  ?chemblEntry up:database <http://purl.uniprot.org/database/ChEMBL> .
}
```

---

Step 10 – Filtering / extras
**Reasoning**
The question asks for "enzymes", and a single enzyme (protein) might catalyze multiple relevant reactions or have multiple catalytic activity annotations. To return each unique protein/ChEMBL pair only once, DISTINCT is needed in the SELECT clause, as seen in the ground truth query.

---

Step 11 – Write the SELECT clause with the variables we determined in step 2.
**Reasoning**
Apply the DISTINCT identified in Step 10 to the variables from Step 2.

'''sparql
SELECT DISTINCT ?protein ?chemblEntry
WHERE {
  # 1. Find relevant reactions in Rhea
  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi rdfs:subClassOf+ CHEBI:26739 .
  }
  # 2. Find human proteins in UniProt that catalyze these reactions
  ?protein up:annotation/up:catalyticActivity ?ca .
  ?ca up:catalyzedReaction ?rhea .
  ?protein up:organism taxon:9606 .
  # 3. Ensure these proteins have a ChEMBL annotation
  ?protein rdfs:seeAlso ?chemblEntry .
  ?chemblEntry up:database <http://purl.uniprot.org/database/ChEMBL> .
}
```

---

Step 12 – Namespace prefixes
**Reasoning**
Define the prefixes. For the target endpoint (rh) use the the URI we identified in step 4.
The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint (provided in the input context) through which the federated query should be initiated.

```sparql
#https://sparql.uniprot.org/sparql
PREFIX CHEBI: <http://purl.obolibrary.org/obo/CHEBI_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rh: <http://rdf.rhea-db.org/>
PREFIX taxon: <http://purl.uniprot.org/taxonomy/>
PREFIX up: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?protein ?chemblEntry
WHERE {
  SERVICE <https://sparql.rhea-db.org/sparql> {
    ?rhea rh:side/rh:contains/rh:compound/rh:chebi rdfs:subClassOf+ CHEBI:26739 .
  }
  ?protein up:annotation/up:catalyticActivity ?ca .
  ?ca up:catalyzedReaction ?rhea .
  ?protein up:organism taxon:9606 .
  ?protein rdfs:seeAlso ?chemblEntry .
  ?chemblEntry up:database <http://purl.uniprot.org/database/ChEMBL> .
}
```
"""
}
]