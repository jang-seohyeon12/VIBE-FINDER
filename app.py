# app.py (최종 버전)

import os
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__) # static_folder 옵션을 일부러 제거했습니다.

# --- 스포티파이 개발자 계정에서 발급받은 ID와 Secret을 입력 ---
SPOTIPY_CLIENT_ID = 'f74ed565294044ab9f9563e20c04d8bd'
SPOTIPY_CLIENT_SECRET = '1107dd47e5c047bfa5314dc4ea37569b'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# --- 웹사이트 첫 페이지를 보여주는 기능 ---
@app.route('/')
def home():
    return render_template('index.html')


# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 이 부분이 핵심입니다 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# /static/ 경로의 파일을 직접 찾아서 보내주는 새로운 기능
@app.route('/static/<path:filename>')
def serve_static(filename):
    # app.py가 있는 폴더를 기준으로 'static' 폴더의 경로를 계산
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # static 폴더 안에서 요청된 파일을 찾아서 보내줌
    return send_from_directory(os.path.join(root_dir, 'static'), filename)
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲


# --- 기분별 음악 추천 API 기능 ---
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


# --- 서버 실행 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)