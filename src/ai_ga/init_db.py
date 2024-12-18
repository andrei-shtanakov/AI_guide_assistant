# init_db.py
from ai_ga.embeddings.bert import BertEmbedder
from ai_ga.storage.pinecone_db import PineconeStorage
from ai_ga.analyzer.config import ConfigAnalyzer
from ai_ga.patterns.loader import PatternLoader, ConfigPattern


# Inicializationing components as global variables
embedder = BertEmbedder()
storage = PineconeStorage()
pattern_loader = PatternLoader()
analyzer = None

def init_vector_db_indexes():
    global analyzer
    storage.init_index("bert-embedding")
    analyzer = ConfigAnalyzer(embedder, storage, pattern_loader)
    analyzer.load_patterns()
    
if __name__ == '__main__':
    init_vector_db_indexes()
