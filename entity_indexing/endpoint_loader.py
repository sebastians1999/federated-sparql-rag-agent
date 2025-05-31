import time
from typing import List, Dict, Any, Optional
from SPARQLWrapper import SPARQLWrapper, JSON
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import re
from bs4 import BeautifulSoup
import httpx 
import json
import asyncio
import nest_asyncio

def sparql_wrapper_base(
    query: str,
    endpoint_url: str,
    post: bool = False,
    timeout: Optional[int] = 300
) -> Any:
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


def query_sparql_wrapper(
    query: str,
    endpoint_url: str,
    post: bool = False,
    timeout: Optional[int] = 300
) -> Any:
    try:
        asyncio_timeout = timeout + 10 if timeout is not None else 310
        
        # Apply nest_asyncio to allow nesting if an event loop is already running
        nest_asyncio.apply()
        
        try:
            # if a loop is already running (Jupyter)
            loop = asyncio.get_running_loop()
            return loop.run_until_complete(run_with_timeout_enforcement(
                query, endpoint_url, post, timeout, asyncio_timeout
            ))
        except RuntimeError:
            # if no loop is running, use asyncio.run (python script)
            return asyncio.run(run_with_timeout_enforcement(
                query, endpoint_url, post, timeout, asyncio_timeout
            ))
    except Exception as e:
        return e

async def run_with_timeout_enforcement(
    query: str,
    endpoint_url: str,
    post: bool,
    regular_timeout: Optional[int],
    asyncio_timeout: int
) -> Any:
    loop = asyncio.get_running_loop()
    
    try:
        return await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: sparql_wrapper_base(query, endpoint_url, post, regular_timeout)
            ),
            timeout=asyncio_timeout
        )
    except asyncio.TimeoutError:
        return Exception(f"Query timed out after {asyncio_timeout} seconds (enforced by asyncio). Results may be partial.")


# def query_sparql_wrapper(
#     query: str,
#     endpoint_url: str,
#     post: bool = False,
#     timeout: Optional[int] = 300
# ) -> Any:
#     """
#     Execute a SPARQL query on a SPARQL endpoint using SPARQLWrapper.

#     Returns 'error' if an exception occurs during the request.
#     """
#     sparql = SPARQLWrapper(endpoint_url)
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
    
#     if post:
#         sparql.setMethod('POST')
#     else:
#         sparql.setMethod('GET')
    
#     if timeout is not None:
#         sparql.setTimeout(timeout)
    
#     try:
#         results = sparql.query().convert()
#         return results
#     except Exception as e:
#         return e


# def parse_sparql_error(response_text):
#     """
#     Parse SPARQL error responses and extract meaningful error information.
    
#     Args:
#         response_text: The error response text or exception from a SPARQL endpoint
        
#     Returns:
#         A concise error message string containing the error type and details
#     """
    
#     # Check if it's an Exception object
#     if isinstance(response_text, Exception):
#         return f"SPARQL Error: {type(response_text).__name__} - {str(response_text)}"
    
#     # Check if it's an HTTP error response as a string
#     if isinstance(response_text, str):
#         # Extract the status code
#         status_match = re.search(r"Error: (\d+)", response_text)
#         status_code = status_match.group(1) if status_match else "Unknown"
        
#         # Try to parse the HTML if present
#         if "<!DOCTYPE html" in response_text or "<html" in response_text:
#             try:
#                 # Extract HTML part from the response
#                 html_start = response_text.find("<!DOCTYPE") if "<!DOCTYPE" in response_text else response_text.find("<html")
#                 html_part = response_text[html_start:]
                
#                 # Parse with BeautifulSoup
#                 soup = BeautifulSoup(html_part, 'html.parser')
                
#                 # Look for error messages in common locations
#                 # For main error title/heading
#                 error_title = None
#                 for selector in ['.error h2', '.error .page-title', '.page-title', 'section.error h2', 'h2.page-title']:
#                     element = soup.select_one(selector)
#                     if element and element.get_text(strip=True):
#                         error_title = element.get_text(strip=True)
#                         break
                
#                 # For detailed error message
#                 error_details = None
#                 for selector in ['.error p', 'section.error p', 'p']:
#                     element = soup.select_one(selector)
#                     if element and element.get_text(strip=True):
#                         error_details = element.get_text(strip=True)
#                         break
                
#                 # If no specific elements found, try the page title
#                 if not error_title and soup.title:
#                     error_title = soup.title.string
                
#                 # Combine the information
#                 if error_title or error_details:
#                     formatted_error = f"SPARQL Error ({status_code}): "
#                     if error_title:
#                         formatted_error += error_title
#                     if error_details:
#                         if error_title:
#                             formatted_error += " - "
#                         formatted_error += error_details
#                     return formatted_error
                
#                 # Fallback if specific elements weren't found
#                 return f"SPARQL Error ({status_code}): Could not extract specific error details"
                
#             except Exception as e:
#                 # Fallback if HTML parsing fails
#                 return f"SPARQL Error ({status_code}): Could not parse error details - {str(e)}"
        
#         # If no HTML is found, return the original error with status code
#         return f"SPARQL Error ({status_code}): Non-HTML error response"
    
#     # For other types of responses
#     return f"SPARQL Error: Unknown error format - {str(response_text)[:200]}"

# def query_sparql_wrapper(query, endpoint_url, post=False, timeout=300):
    
#     headers = {'Accept': 'application/sparql-results+json'}

#     cli
    
#     try:
#         if post:
#             response = requests.post(
#                 endpoint_url, 
#                 data={'query': query}, 
#                 headers=headers, 
#                 timeout=timeout
#             )
#         else:
#             response = requests.get(
#                 endpoint_url, 
#                 params={'query': query}, 
#                 headers=headers, 
#                 timeout=timeout
#             )
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             error_msg = f"Error: {response.status_code} - {response.text}"
#             return parse_sparql_error(error_msg)
#     except requests.exceptions.Timeout:
#         return f"SPARQL Error: Query timed out after {timeout} seconds"
#     except Exception as e:
#         return parse_sparql_error(e)


    

# def query_sparql_wrapper(query, endpoint_url, post=False, timeout=300):
    
#     headers = {'Accept': 'application/sparql-results+json'}

#     timeouts = httpx.Timeout(
#         connect=10.0, 
#         read=timeout,  
#         write=60.0,    
#         pool=10.0    
#     )
    
#     client = httpx.Client(
#         follow_redirects=True, 
#         timeout=timeouts
#     )
    
#     try:
#         if post:
#             response = client.post(
#                 endpoint_url, 
#                 data={'query': query}, 
#                 headers=headers, 
#             )
#         else:
#             response = client.get(
#                 endpoint_url, 
#                 params={'query': query}, 
#                 headers=headers,
#             )

#         if response.status_code == 200:
#             return response.json()
#         else:
#             error_msg = f"Error: {response.status_code} - {response.text}"
#             parsed_error = parse_sparql_error(error_msg)
#             return Exception(parsed_error)
            
#     except httpx.TimeoutException as e:
#         return e
#     except json.JSONDecodeError as e:
#         return Exception(f"Query timeout likely occurred - received partial results: {str(e)}")
#     except Exception as e:
#         parsed_error = parse_sparql_error(e)
#         return Exception(parsed_error)
#     finally:
#         client.close()


def retrieve_index_data(entity: dict, entities_list: List[Dict], pagination: tuple = None) -> List[Dict]:
    """Retrieve entity data from SPARQL endpoint and format it as dictionaries for the indexing pipeline."""
    query = (
        f"{entity['query']} LIMIT {pagination[0]} OFFSET {pagination[1]}"
        if pagination
        else entity["query"]
    )
    try:
        entities_res = sparql_wrapper_base(query, entity["endpoint"])["results"]["bindings"]
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
