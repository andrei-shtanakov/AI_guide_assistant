from typing import List
from src.ai_ga.patterns.loader import PatternLoader, ConfigPattern
class ConfigAnalyzer:
    def __init__(self, embedder, storage, pattern_loader: PatternLoader):
        self.embedder = embedder
        self.storage = storage
        self.pattern_loader = pattern_loader
    
    def load_patterns(self):
        """Загружает все паттерны в векторную БД."""
        patterns = self.pattern_loader.load_patterns()
        for pattern in patterns:
            self.store_pattern(pattern)
    
    def store_pattern(self, pattern: ConfigPattern):
        """Сохраняет один паттерн в векторную БД."""
        embedding = self.embedder.get_embedding(pattern.config)
        metadata = {
            "original_text": pattern.config,
            "description": pattern.description,
            "severity": pattern.severity,
            "recommendations": pattern.recommendations
        }
        self.storage.store_vector(pattern.id, embedding, metadata)

    def analyze(self, config_text: str, top_k: int = 5):
        """
        Анализирует конфигурацию и возвращает похожие проблемные паттерны.
    
        Args:
            config_text (str): Текст конфигурации для анализа
            top_k (int): Количество похожих паттернов для возврата
        
        Returns:
            list: Список найденных паттернов с их метаданными и score
        """
        # Получаем эмбеддинг для анализируемой конфигурации
        query_embedding = self.embedder.get_embedding(config_text)
        
        # Ищем похожие паттерны
        results = self.storage.search(query_embedding, top_k=top_k)
        
        return [{
            'id': match.id,
            'score': match.score,
            'description': match.metadata['description'],
            'severity': match.metadata['severity'],
            'recommendations': match.metadata['recommendations'],
            'original_text': match.metadata['original_text']
        } for match in results.matches]