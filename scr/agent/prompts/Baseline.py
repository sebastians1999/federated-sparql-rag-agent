from .general import INTRODUCTION_PROMPT

BASELINE_PROMPT = (
    INTRODUCTION_PROMPT
    + """
Potential entities extracted from the user question: {{potential_entities}}

Potential classes extracted from the user question: {{potential_classes}}

**Task:**
Generate a federated SPARQL query to answer the user question, utilizing the provided inputs (question, classes, entities).

**Requirements:**

1.**Output Format:** Provide the generated SPARQL query inside a single markdown code block with the "sparql" language tag (````sparql ... ````).

2. **Endpoint Comment:** - The *very first line* inside the code block *must* be a comment containing the URL of the *primary* SPARQL endpoint through which the federated query should be initiated.
                         - Include only this single primary endpoint URL comment at the start. No other text on this line or preceding it within the code block.                                           
"""
)