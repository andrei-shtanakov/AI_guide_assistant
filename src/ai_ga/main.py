# app.py
from flask import Flask, request, render_template, jsonify
from ai_ga.embeddings.bert import BertEmbedder
from ai_ga.storage.pinecone_db import PineconeStorage
from ai_ga.analyzer.config import ConfigAnalyzer
from ai_ga.patterns.loader import PatternLoader, ConfigPattern

app = Flask(__name__)

# Инициализация компонентов как глобальных переменных
embedder = BertEmbedder()
storage = PineconeStorage()
pattern_loader = PatternLoader()
analyzer = None

def init_analyzer():
    global analyzer
    storage.init_index("bert-embedding")
    analyzer = ConfigAnalyzer(embedder, storage, pattern_loader)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    config_text = request.form.get('config')
    if not config_text:
        return jsonify({'error': 'No configuration provided'})
    
    results = analyzer.analyze(config_text)
    return jsonify({'results': results})

if __name__ == '__main__':
    init_analyzer()
    app.run(debug=True, host='0.0.0.0')  