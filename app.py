from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# --- 스포티파이 개발자 계정에서 발급받은 ID와 Secret을 입력 ---
SPOTIPY_CLIENT_ID = 'f74ed565294044ab9f9563e20c04d8bd'
SPOTIPY_CLIENT_SECRET = '1107dd47e5c047bfa5314dc4ea37569b'

# Spotipy 객체 설정
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# --- 기분별 음악 추천 로직 ---
@app.route('/api/mood-recommend')
def recommend_by_mood():
    mood = request.args.get('mood')
    
    # 기분과 스포티파이 'Audio Features'를 매핑
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

    # 스포티파이에 추천 요청
    # seed_genres: 추천의 기반이 될 장르 (다양하게 설정 가능)
    results = sp.recommendations(seed_genres=['k-pop', 'pop'], limit=20, **params)
    
    # 프론트엔드로 보낼 데이터 가공
    tracks = []
    for track in results['tracks']:
        if track['preview_url']: # 30초 미리듣기가 있는 곡만 포함
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album_art': track['album']['images'][0]['url'],
                'preview_url': track['preview_url']
            })
            
    return jsonify({"tracks": tracks})

# --- 노래 분위기 검색 로직 (간단한 키워드 기반) ---
@app.route('/api/vibe-search')
def search_by_vibe():
    query = request.args.get('q', '') # 예: "신나지만 시끄럽지 않은 노래"
    
    params = {'target_valence': 0.5, 'target_energy': 0.5} # 기본값
    
    # 키워드 분석 (간단한 버전)
    if '신나는' in query:
        params['target_valence'] = 0.8
        params['target_energy'] = 0.7
    if '조용한' in query:
        params['target_energy'] = 0.2
        params['target_acousticness'] = 0.8
    if '슬픈' in query:
        params['target_valence'] = 0.2
    if '시끄럽지 않은' in query:
        params['target_energy'] = max(0.4, params.get('target_energy', 0.5) - 0.3) # 기존 에너지에서 조금 빼기
        
    # 위와 동일하게 sp.recommendations 호출 및 데이터 가공
    # ... (코드는 위 mood-recommend와 유사) ...
    
    return jsonify({"tracks": []}) # 임시 반환

if __name__ == '__main__':
    app.run(debug=True)
