import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

# --- 스포티파이 개발자 계정 정보 ---
SPOTIPY_CLIENT_ID = 'f74ed565294044ab9f9563e20c04d8bd'
SPOTIPY_CLIENT_SECRET = '1107dd47e5c047bfa5314dc4ea37569b'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# --- 라우트(경로) 설정 ---
@app.route('/')
def home():
    return render_template('index.html')

# static 파일 수동 서빙 (절대 경로 사용)
@app.route('/static/<path:filename>')
def serve_static(filename):
    static_dir_path = '/workspace/VIBE-FINDER/static'
    return send_from_directory(static_dir_path, filename)

@app.route('/api/mood-recommend')
def recommend_by_mood():
    mood = request.args.get('mood')
    mood_params = {
        'joy':        {'target_valence': 0.8, 'target_energy': 0.8},
        'sadness':    {'target_valence': 0.2, 'target_energy': 0.3},
        'anger':      {'target_valence': 0.2, 'target_energy': 0.9},
        'excitement': {'target_valence': 0.9, 'target_energy': 0.9},
        'gloominess': {'target_valence': 0.3, 'target_energy': 0.2},
        'fatigue':    {'target_valence': 0.5, 'target_energy': 0.1}
    }
    params = mood_params.get(mood, {})
    if not params:
        return jsonify({"error": "Invalid mood"}), 400

    try:
        results = sp.recommendations(seed_genres=['k-pop', 'pop', 'acoustic'], limit=20, **params)
        tracks = []
        for track in results['tracks']:
            if track['preview_url']:
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album_art': track['album']['images'][0]['url'],
                    'preview_url': track['preview_url']
                })
        return jsonify({"tracks": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 서버 실행 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
