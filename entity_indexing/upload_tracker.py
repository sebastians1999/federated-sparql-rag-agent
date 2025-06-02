import os
import json
import uuid
from typing import List, Dict, Optional, Callable, Set, Union

class UploadTracker:
    
    """Tracks entity URIs that have been uploaded to a vector database.
    
    This class maintains a persistent record of uploaded entity URIs in a JSON file,
    allowing the indexing process to skip already processed entities and resume
    interrupted indexing operations efficiently.
    """
    def __init__(self, collection_name: str, log_dir: str = "/upload_logs"):
        """Initialize the upload tracker for a specific collection.
        
        Args:
            collection_name: Name of the vector database collection being tracked
            log_dir: Directory where upload logs will be stored
        """
        self.collection_name = collection_name
        self.log_dir = log_dir
        self.log_file = os.path.join(self.log_dir, f"{collection_name}_uploaded_ids.json")
        self.uploaded_ids = set()
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        self._load_log()
        


    
    def _load_log(self):
        """Load the previously uploaded entity IDs from the log file.
        
        If the log file exists, loads the set of uploaded IDs from it.
        If the file doesn't exist or there's an error, initializes an empty set.
        """
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.uploaded_ids = set(json.load(f))
                print(f"Loaded {len(self.uploaded_ids)} previously uploaded IDs from log")
            except Exception as e:
                print(f"Error loading upload log: {str(e)}")
                self.uploaded_ids = set()
        else:
            print("No existing upload log found, starting fresh")
            self.uploaded_ids = set()




    def _save_log(self):
        """Save the current set of uploaded entity IDs to the log file.
        
        Converts the set to a list for JSON serialization and handles any errors
        that might occur during saving.
        """
        try:
            with open(self.log_file, 'w') as f:
                json.dump(list(self.uploaded_ids), f)
        except Exception as e:
            print(f"Error saving upload log: {str(e)}")
    


    def generate_uuid_from_uri(self, uri: str) -> str:
        """Generate a deterministic UUID based on the URI for consistent tracking.
        
        Args:
            uri: The entity URI to generate a UUID for
            
        Returns:
            A string representation of the UUID generated from the URI
        """
        return str(uuid.uuid5(uuid.NAMESPACE_URL, uri))
        



    def is_uploaded(self, uuid_str: str) -> bool:
        """Check if an entity has already been uploaded based on its UUID.
        
        Args:
            uuid_str: UUID string to check
            
        Returns:
            True if the entity has been uploaded, False otherwise
        """
        return uuid_str in self.uploaded_ids
       
       

    def mark_as_uploaded(self, uuid_list: List[str]):
        """Mark a list of entities as uploaded by adding their UUIDs to the tracking set.
        
        Args:
            uuid_list: List of UUID strings to mark as uploaded
        """
        self.uploaded_ids.update(uuid_list)
        self._save_log()



    def get_uploaded_count(self) -> int:
        """Get the total number of entities that have been uploaded.
        
        Returns:
            Count of uploaded entities
        """
        return len(self.uploaded_ids)
    


    def extract_uri(self, doc: Dict) -> str:
        """Extract the URI from a document, handling different data formats.
        
        Supports both direct string values and SPARQL result format with 'value' key.
        
        Args:
            doc: Document dictionary containing a 'uri' field
            
        Returns:
            The extracted URI as a string
        """
        uri = doc.get('uri')
        if isinstance(uri, dict) and 'value' in uri:
            return uri['value']
        return uri
    


    def filter_new_entities(self, documents: List[Dict]) -> List[Dict]:
        """Filter a list of documents to include only entities that haven't been uploaded yet.
        
        Args:
            documents: List of document dictionaries to filter
            
        Returns:
            List containing only documents that haven't been uploaded
        """
        new_docs = []
        for doc in documents:
            uri = self.extract_uri(doc)
            uuid_str = self.generate_uuid_from_uri(uri)
            if not self.is_uploaded(uuid_str):
                new_docs.append(doc)
                
        skipped = len(documents) - len(new_docs)
        if skipped > 0:
            print(f"Skipping {skipped} already uploaded entities")
            
        return new_docs



def process_batch(tracker: UploadTracker, batch: List[Dict], process_func: Callable):
    """Process a batch of entities and mark them as uploaded if successful.
    
    This function handles the workflow of:
    1. Extracting URIs and generating UUIDs for each document in the batch
    2. Processing the batch using the provided function
    3. Marking the batch as uploaded if processing succeeds
    4. Handling any errors that occur during processing
    
    Args:
        tracker: UploadTracker instance to track uploaded entities
        batch: List of document dictionaries to process
        process_func: Function to call for processing the batch
        
    Returns:
        True if batch was processed successfully, False otherwise
    """
    batch_uuids = []
    
    for doc in batch:
        uri = tracker.extract_uri(doc)
        uuid_str = tracker.generate_uuid_from_uri(uri)
        batch_uuids.append(uuid_str)
    
    try:
        process_func(batch)
        tracker.mark_as_uploaded(batch_uuids)
        print(f"Batch processed - Total uploaded: {tracker.get_uploaded_count()}")
        return True
    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        return False
