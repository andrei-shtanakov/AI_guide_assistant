from pinecone.grpc import PineconeGRPC, GRPCClientConfig
from pinecone import ServerlessSpec
import time
import os
from typing import List, Dict, Any, Optional

class PineconeStorage:
    def __init__(self, api_key="pclocal", host="http://pinecone:5080"):
        self.pc = PineconeGRPC(api_key=api_key, host=host)
        self.index = None
        
    def init_index(self, index_name, dimension=768):
        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            
        while not self.pc.describe_index(index_name).status['ready']:
            time.sleep(1)
            
        index_host = self.pc.describe_index(index_name).host
        self.index = self.pc.Index(
            host=index_host, 
            grpc_config=GRPCClientConfig(secure=False)
        )
    
    def store_vector(self, vector_id, vector, metadata):
        self.index.upsert([(vector_id, vector, metadata)])
    
    def search(self, vector, top_k=5):
        return self.index.query(vector, top_k=top_k, include_metadata=True)