# app.py
from flask import Flask, request, render_template, jsonify
from ai_ga.embeddings.bert import BertEmbedder
from ai_ga.storage.pinecone_db import PineconeStorage
from ai_ga.analyzer.config import ConfigAnalyzer
from ai_ga.patterns.loader import PatternLoader, ConfigPattern
from ai_ga.ai_services.ai_integration import AIAnalyzer

app = Flask(__name__)

# Инициализация компонентов
embedder = BertEmbedder()
storage = PineconeStorage()
pattern_loader = PatternLoader()
ai_analyzer = AIAnalyzer()
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
    analysis_type = request.form.get('analysis_type', 'pattern')  # pattern, openai, или claude
    
    if not config_text:
        return jsonify({'error': 'No configuration provided'})
    
    # Получаем результаты паттерн-анализа
    pattern_results = analyzer.analyze(config_text)
    
    if analysis_type == 'pattern':
        return jsonify({'results': pattern_results})
    
    # Преобразуем pattern_results в текстовый формат для AI
    pattern_results_text = '\n'.join([
        f"Pattern {i+1}:\n" +
        f"ID: {result['id']}\n" +
        f"Description: {result['description']}\n" +
        f"Severity: {result['severity']}\n" +
        f"Recommendations: {', '.join(result['recommendations'])}\n" +
        f"Example: {result['original_text']}\n"
        for i, result in enumerate(pattern_results)
    ])
    
    try:
        if analysis_type == 'openai':
            ai_response = ai_analyzer.analyze_with_openai(config_text, pattern_results_text)
        else:  # claude
            ai_response = ai_analyzer.analyze_with_claude(config_text, pattern_results_text)
            
        return jsonify({
            'results': pattern_results,
            'ai_analysis': ai_response
        })
    
    except Exception as e:
        return jsonify({
            'results': pattern_results,
            'error': f'AI analysis failed: {str(e)}'
        })

if __name__ == '__main__':
    init_analyzer()
    app.run(debug=True, host='0.0.0.0')