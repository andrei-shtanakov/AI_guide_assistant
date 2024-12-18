from typing import List
from src.ai_ga.patterns.loader import PatternLoader, ConfigPattern
class ConfigAnalyzer:
    def __init__(self, embedder, storage, pattern_loader: PatternLoader):
        self.embedder = embedder
        self.storage = storage
        self.pattern_loader = pattern_loader
    
    def load_patterns(self):
        """Loads all patterns into the vector database."""
        patterns = self.pattern_loader.load_patterns()
        for pattern in patterns:
            self.store_pattern(pattern)
    
    def store_pattern(self, pattern: ConfigPattern):
        """Stores a single pattern into the vector database."""
        embedding = self.embedder.get_embedding(pattern.config)
        metadata = {
            "original_text": pattern.config,
            "description": pattern.description,
            "severity": pattern.severity,
            "recommendations": pattern.recommendations
        }
        self.storage.store_vector(pattern.id, embedding, metadata)

    def analyze(self, config_text: str, top_k: int = 2):
        """
        Analyzes the configuration and returns similar problematic patterns.
    
        Args:
            config_text (str): Configuration text to analyze
            top_k (int): Number of similar patterns to return.

        Returns:
            list: Список найденных паттернов с их метаданными и score
        """
        # Get embedding for the configuration being analyzed
        query_embedding = self.embedder.get_embedding(config_text)
    
        # Search for similar patterns
        results = self.storage.search(query_embedding, top_k=top_k)
    
        return [{
            'id': match.id,
            'score': match.score,
            'description': match.metadata['description'],
            'severity': match.metadata['severity'],
            'recommendations': match.metadata['recommendations'],
            'original_text': match.metadata['original_text']
        } for match in results.matches]