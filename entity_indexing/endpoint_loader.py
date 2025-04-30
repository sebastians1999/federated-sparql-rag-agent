import time
from typing import List, Dict, Any, Optional
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Optional, Any

# import logging 


# logging.basicConfig(level=logging.INFO)

def query_sparql_wrapper(
    query: str,
    endpoint_url: str,
    post: bool = False,
    timeout: Optional[int] = None
) -> Any:
    """
    Execute a SPARQL query on a SPARQL endpoint using SPARQLWrapper.

    Returns 'error' if an exception occurs during the request.
    """
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    if post:
        sparql.setMethod('POST')
    else:
        sparql.setMethod('GET')
    
    if timeout is not None:
        sparql.setTimeout(timeout)
    
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        return e



def retrieve_index_data(entity: dict, entities_list: List[Dict], pagination: tuple = None) -> List[Dict]:
    """Retrieve entity data from SPARQL endpoint and format it as dictionaries for the indexing pipeline."""
    query = (
        f"{entity['query']} LIMIT {pagination[0]} OFFSET {pagination[1]}"
        if pagination
        else entity["query"]
    )
    try:
        entities_res = query_sparql_wrapper(query, entity["endpoint"])["results"]["bindings"]
    except Exception as e:
        print(f"Error querying endpoint {entity['endpoint']}: {str(e)}")
        return None
    
    print(f"Found {len(entities_res)} entities for {entity['label']} in {entity['endpoint']}")
    #print(f"Entities: {entities_res[:1]}")
    
    for entity_res in entities_res:
        # Create dictionary format compatible with entity_indexing_pipeline_v3.py
        entities_list.append({
            "label": entity_res["label"]["value"],
            "uri": entity_res["uri"]["value"],
            "endpoint_url": entity["endpoint"],
            "entity_type": entity_res["label"]["type"],
            "description": entity.get("description", "")
        })
    #print(entities_list[0:5])

    return entities_res

def load_entities_from_endpoints(entities_config: List[Dict] = None, max_results_per_batch: int = 200000):
    
    flattened_configs = []
    start_time = time.time()
    
    if entities_config is not None:
        for entity_group in entities_config:
            if isinstance(entity_group, dict) and any(isinstance(v, dict) for v in entity_group.values()):
                for entity_name, entity_config in entity_group.items():
                    flattened_configs.append(entity_config)
            else:
                flattened_configs.append(entity_group)

    print(f"Flattened {len(flattened_configs)} entities for indexing")
    print(f"Flattened entities: {flattened_configs}")
    
    entities_for_indexing = []
    
    for entity in flattened_configs:
        print(f"Loading entities from {entity['endpoint']} for {entity['label']}...")
        
        if entity.get("pagination", False):
            batch_size = max_results_per_batch
            offset = 0
            batch_results = True
            
            while batch_results:
                batch_results = retrieve_index_data(entity, entities_for_indexing, (batch_size, offset))
                if batch_results:
                    offset += batch_size
                    print(f"  Retrieved {len(batch_results)} entities, total so far: {len(entities_for_indexing)}")
        else:
            retrieve_index_data(entity, entities_for_indexing)
    
    elapsed_time = (time.time() - start_time) / 60
    print(f"Done querying SPARQL endpoints in {elapsed_time:.2f} minutes, retrieved {len(entities_for_indexing)} entities")
    
    return entities_for_indexing
