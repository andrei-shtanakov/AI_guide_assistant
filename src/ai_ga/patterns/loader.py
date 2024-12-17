import yaml
from pathlib import Path
from typing import List, Dict, Any

class ConfigPattern:
    def __init__(self, id: str, config: str, description: str, 
                 severity: str, recommendations: List[str]):
        self.id = id
        self.config = config
        self.description = description
        self.severity = severity
        self.recommendations = recommendations

class PatternLoader:
    def __init__(self, patterns_dir: str = None):
        if patterns_dir is None:
            patterns_dir = Path(__file__).parent / 'data'
        self.patterns_dir = Path(patterns_dir)

    def load_patterns(self) -> List[ConfigPattern]:
        """Загружает все паттерны из YAML файла."""
        patterns_file = self.patterns_dir / 'patterns.yaml'
        
        with open(patterns_file, 'r') as f:
            patterns_data = yaml.safe_load(f)
        
        return [
            ConfigPattern(
                id=pattern['id'],
                config=pattern['config'],
                description=pattern['description'],
                severity=pattern['severity'],
                recommendations=pattern['recommendations']
            )
            for pattern in patterns_data
        ]

    def add_pattern(self, pattern: ConfigPattern):
        """Добавляет новый паттерн в YAML файл."""
        patterns_file = self.patterns_dir / 'patterns.yaml'
        
        # Загружаем существующие паттерны
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                patterns = yaml.safe_load(f) or []
        else:
            patterns = []

        # Добавляем новый паттерн
        patterns.append({
            'id': pattern.id,
            'config': pattern.config,
            'description': pattern.description,
            'severity': pattern.severity,
            'recommendations': pattern.recommendations
        })

        # Сохраняем обновленный список
        with open(patterns_file, 'w') as f:
            yaml.safe_dump(patterns, f)