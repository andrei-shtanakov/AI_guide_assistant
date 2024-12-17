from embeddings.bert import BertEmbedder
from storage.pinecone_db import PineconeStorage
from analyzer.config import ConfigAnalyzer

def main():
    # Инициализация компонентов
    embedder = BertEmbedder()
    storage = PineconeStorage()
    storage.init_index("bert-embedding")
    analyzer = ConfigAnalyzer(embedder, storage)
    
    # Пример использования
    analyzer.store_pattern(
        config_text="""
        FROM ubuntu:latest
        USER root
        EXPOSE 22
        """,
        pattern_id="docker_root_unsafe_001",
        description="Использование root пользователя в контейнере является небезопасной практикой",
        severity="HIGH",
        recommendations=[
            "Создайте и используйте непривилегированного пользователя",
            "Добавьте USER <non-root-user> в Dockerfile",
            "Убедитесь, что приложение может работать без root прав"
        ]
    )
    
    new_config = """
    FROM python:3.9
    USER root
    EXPOSE 22
    CMD ["python", "app.py"]
    """
    
    analyzer.analyze(new_config)

if __name__ == "__main__":
    main()