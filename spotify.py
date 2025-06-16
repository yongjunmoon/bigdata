import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Spotify API 인증
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
))

# Spotify Global Top 50 플레이리스트 ID
playlist_id = "37i9dQZEVXbMDoHDwVN2tF"

# 플레이리스트 트랙 가져오기
results = sp.playlist_items(playlist_id, additional_types=['track'])

tracks = []
for item in results['items']:
    track = item['track']
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    
    # 아티스트 장르 가져오기
    artist_id = track['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    genre = artist_info['genres'][0] if artist_info['genres'] else 'Unknown'
    
    tracks.append({
        'Title': track_name,
        'Artist': artist_name,
        'Genre': genre
    })

# 데이터프레임 생성
df = pd.DataFrame(tracks)
print(df.head())

# 장르 분포 시각화
genre_counts = df['Genre'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%')
plt.title("🎵 Spotify Global Top 50 - Genre Distribution")
plt.axis('equal')
plt.show()

# 아티스트 워드클라우드
artist_string = ' '.join(df['Artist'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(artist_string)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('🔥 Spotify Global Top Artists (2025)')
plt.show()
