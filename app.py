# app.py (수정된 최종 버전)

from flask import Flask, request, jsonify, render_template # render_template 추가!
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# --- 스포티파이 개발자 계정에서 발급받은 ID와 Secret을 입력 ---
SPOTIPY_CLIENT_ID = 'f74ed565294044ab9f9563e20c04d8bd'
SPOTIPY_CLIENT_SECRET = '1107dd47e5c047bfa5314dc4ea37569b'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# 웹사이트의 첫 페이지 ('/')로 접속했을 때 index.html 파일을 보여주는 기능
@app.route('/')
def home():
    # templates 폴더에 있는 index.html을 불러와서 사용자에게 보여줌
    return render_template('index.html')


# --- 기분별 음악 추천 로직 ---
@app.route('/api/mood-recommend')
def recommend_by_mood():
    mood = request.args.get('mood')
    
    mood_params = {
        'joy':        {'target_valence': 0.8, 'target_energy': 0.8},
        'sadness':    {'target_valence': 0.2, 'target_energy': 0.3},
        'anger':      {'target_valence': 0.2, 'target_energy': 0.9, 'target_tempo': 150},
        'excitement': {'target_valence': 0.9, 'target_energy': 0.9, 'target_tempo': 140},
        'gloominess': {'target_valence': 0.3, 'target_energy': 0.2, 'target_tempo': 80},
        'fatigue':    {'target_valence': 0.5, 'target_energy': 0.1, 'target_acousticness': 0.8}
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

# (다른 API 기능들은 그대로 두면 됩니다)

if __name__ == '__main__':
    # 외부에서 접속할 수 있도록 host='0.0.0.0' 추가
    # port는 사용하는 환경에 따라 8080, 5001 등으로 변경 가능
    app.run(host='0.0.0.0', port=5000, debug=True)
