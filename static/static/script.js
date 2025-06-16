// 예시: 기분 버튼 클릭 시 서버에 노래 추천 요청
document.querySelectorAll('.mood-buttons button').forEach(button => {
    button.addEventListener('click', () => {
        const mood = button.dataset.mood;
        
        // fetch를 사용해 우리 서버의 /api/mood-recommend 주소로 요청을 보냄
        fetch(`/api/mood-recommend?mood=${mood}`)
            .then(response => response.json())
            .then(data => {
                displayTracks(data.tracks); // 받은 노래 데이터로 화면 업데이트
            });
    });
});

// 서버로부터 받은 트랙 정보를 화면에 표시하는 함수
function displayTracks(tracks) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // 이전 결과 초기화

    tracks.forEach(track => {
        const trackElement = document.createElement('div');
        trackElement.className = 'track';

        // 앨범 커버, 제목, 아티스트, 30초 미리듣기 플레이어
        trackElement.innerHTML = `
            <img src="${track.album_art}" alt="${track.name}">
            <div>
                <strong>${track.name}</strong>
                <p>${track.artist}</p>
            </div>
            <audio controls src="${track.preview_url}"></audio>
        `;
        resultsDiv.appendChild(trackElement);
    });
}
