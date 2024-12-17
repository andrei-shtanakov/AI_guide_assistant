from ai_ga.embeddings.bert import BertEmbedder
from ai_ga.storage.pinecone_db import PineconeStorage
from ai_ga.analyzer.config import ConfigAnalyzer
from ai_ga.patterns.loader import PatternLoader, ConfigPattern

def main():
    # Инициализация компонентов
    embedder = BertEmbedder()
    storage = PineconeStorage()
    storage.init_index("bert-embedding")
    
    pattern_loader = PatternLoader()
    analyzer = ConfigAnalyzer(embedder, storage, pattern_loader)
    
    # Загрузка всех паттернов в БД
    analyzer.load_patterns()
    
    # Добавление нового паттерна
    new_pattern = ConfigPattern(
        id="docker_no_healthcheck_001",
        config="FROM python:3.9\nCMD ['python', 'app.py']",
        description="Отсутствует проверка здоровья контейнера",
        severity="LOW",
        recommendations=[
            "Добавьте HEALTHCHECK в Dockerfile",
            "Настройте соответствующие параметры проверки"
        ]
    )
    pattern_loader.add_pattern(new_pattern)
    analyzer.store_pattern(new_pattern)
    
    # Анализ конфигурации
    config_to_analyze = """
    FROM python:3.9
    USER root
    EXPOSE 22
    CMD ["python", "app.py"]
    """
    results = analyzer.analyze(config_to_analyze)

     # Вывод результатов
    for match in results:
        print(f"\nНайден похожий проблемный паттерн (score: {match['score']})")
        print(f"Проблемный паттерн ID: {match['id']}")
        print(f"Описание проблемы: {match['description']}")
        print(f"Уровень критичности: {match['severity']}")
        print("\nРекомендации:")
        for rec in match['recommendations']:
            print(f"- {rec}")
        print("\nПример проблемного кода:")
        print(match['original_text'])

if __name__ == "__main__":
    main()