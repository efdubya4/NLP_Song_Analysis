from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from modules.lyric_analysis import LyricAnalyzer
from modules.prediction import HitPredictor
import os

app = Flask(__name__)

# 1. Configure CORS with explicit settings
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 86400  # Cache preflight response for 24 hours
    }
})

# 2. Add after_request handler for additional headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Initialize components
lyric_analyzer = LyricAnalyzer()
hit_predictor = HitPredictor()

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:3000', supports_credentials=True)
def analyze_song():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'preflight'}), 200
    
    try:
        data = request.get_json()
        
        # Extract form data with validation
        danceability = float(data.get('danceability', 0.5))
        energy = float(data.get('energy', 0.5))
        tempo = float(data.get('tempo', 120))
        valence = float(data.get('valence', 0.5))
        lyrics = str(data.get('lyrics', ''))
        genre = str(data.get('genre', 'Pop'))
        
        # Process lyrics if provided
        lyrics_analysis = {}
        if lyrics:
            import pandas as pd
            df = pd.DataFrame({'lyrics': [lyrics]})
            df_with_analysis = lyric_analyzer.add_analysis_features(df)
            lyrics_analysis = df_with_analysis.iloc[0].to_dict()
        
        # Create prediction
        prediction_result = {
            'probability_top_chart': min(0.99, danceability * 0.3 + energy * 0.25 + valence * 0.2 + (tempo/200) * 0.15),
            'confidence': 0.8,
            'analysis': {
                'danceability_impact': danceability * 100 / 2,
                'energy_impact': energy * 100 / 2,
                'valence_impact': valence * 100 / 2,
                'tempo_impact': (tempo/200) * 50,
                'lyrics_impact': len(lyrics.split()) / 10 if lyrics else 0
            }
        }
        
        return jsonify(prediction_result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analyses', methods=['GET', 'OPTIONS'])
@cross_origin(origin='http://localhost:3000')
def get_analyses():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'preflight'}), 200
    
    saved_analyses = [
        {
            'id': 1,
            'title': 'Summer Hit',
            'artist': 'User',
            'date': '2023-06-15',
            'score': 78.5
        },
        {
            'id': 2,
            'title': 'Winter Ballad',
            'artist': 'User',
            'date': '2023-05-22',
            'score': 65.2
        }
    ]
    
    return jsonify(saved_analyses), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)