class ConfigAnalyzer:
    def __init__(self, embedder, storage):
        self.embedder = embedder
        self.storage = storage
    
    def store_pattern(self, config_text, pattern_id, description, severity, recommendations):
        embedding = self.embedder.get_embedding(config_text)
        metadata = {
            "original_text": config_text,
            "description": description,
            "severity": severity,
            "recommendations": recommendations
        }
        self.storage.store_vector(pattern_id, embedding, metadata)
    
    def analyze(self, config_text):
        embedding = self.embedder.get_embedding(config_text)
        results = self.storage.search(embedding)
        
        for match in results.matches:
            print(f"\nНайден похожий проблемный паттерн (score: {match.score})")
            print(f"Проблемный паттерн ID: {match.id}")
            print(f"Описание проблемы: {match.metadata['description']}")
            print(f"Уровень критичности: {match.metadata['severity']}")
            print("\nРекомендации:")
            for rec in match.metadata['recommendations']:
                print(f"- {rec}")
            print("\nПример проблемного кода:")
            print(match.metadata['original_text'])