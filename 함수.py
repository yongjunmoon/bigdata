import requests
from bs4 import BeautifulSoup
import random

def get_melon_chart(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        songs = []
        for entry in soup.select('tr.lst50, tr.lst100'):
            rank = entry.select_one('span.rank').get_text()
            title = entry.select_one('div.ellipsis.rank01 a').get_text()
            artist = entry.select_one('div.ellipsis.rank02 a').get_text()
            songs.append((rank, title, artist))
        return songs
    except requests.exceptions.RequestException as e:
        print(f"웹 요청 오류: {e}")
        return None
    except AttributeError as e:
        print(f"데이터 추출 오류: {e}")
        return None

def print_chart(songs, limit=100):
    if songs:
        for song in songs[:limit]:
            print(f"{song[0]}. {song[1]} - {song[2]}")
    else:
        print("차트 정보를 가져올 수 없습니다.")

def recommend_song(songs):
    if songs:
        ai_song = random.choice(songs)
        print(f"추천곡은 {ai_song[1]} - {ai_song[2]} 입니다.")
    else:
        print("추천할 곡이 없습니다.")

def search_artist(songs, artist_name):
    if songs:
        found_songs = [song for song in songs if artist_name in song[2]]
        if found_songs:
            print(f"'{artist_name}'의 노래 목록:")
            for song in found_songs:
                print(f"{song[0]}. {song[1]} - {song[2]}")
        else:
            print(f"'{artist_name}'의 노래를 찾을 수 없습니다.")
    else:
        print("검색할 곡이 없습니다.")

def save_chart_to_file(songs, filename="melon_chart.txt"):
    if songs:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("멜론 실시간 차트 TOP 100\n")
                f.write("=====================\n")
                for song in songs:
                    f.write(f"{song[0]}. {song[1]} - {song[2]}\n")
            print(f"멜론 차트 TOP 100이 '{filename}'에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 오류: {e}")
    else:
        print("저장할 차트 정보가 없습니다.")

if __name__ == "__main__":
    url = 'https://www.melon.com/chart/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    songs = get_melon_chart(url, headers)

    print("================")
    print("1. 멜론 100 출력")
    print("2. 멜론 50 출력")
    print("3. 멜론 10 출력")
    print("4. AI 추천곡 출력")
    print("5. 가수 이름 검색")
    print("6. 멜론 100 파일에 저장")

    choice = input("메뉴 선택 (숫자 입력): ")

    if choice == '1':
        print_chart(songs)
    elif choice == '2':
        print_chart(songs, limit=50)
    elif choice == '3':
        print_chart(songs, limit=10)
    elif choice == '4':
        recommend_song(songs)
    elif choice == '5':
        artist_name = input("가수 이름 입력: ")
        search_artist(songs, artist_name)
    elif choice == '6':
        save_chart_to_file(songs)
    else:
        print("1~6까지의 숫자를 입력해 주세요.")
