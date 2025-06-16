from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 네이버 월요 웹툰 URL
url = 'https://comic.naver.com/webtoon?tab=mon'

try:
    # 크롬 옵션 설정 (선택사항)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 헤드리스 모드 (브라우저 창이 보이지 않음)
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 크롬 드라이버 설정
    service = Service('chromedriver.exe')  # 크롬 드라이버 경로를 적절히 수정하세요
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"웹 드라이버 초기화 오류: {e}")
    print("ChromeDriver 경로를 확인하거나 시스템 PATH에 추가했는지 확인하세요.")
    exit()

# 웹 페이지 열기
driver.get(url)

# 페이지 로딩을 기다릴 시간
print("페이지 로딩 중...")
time.sleep(5)  # 페이지가 충분히 로드될 때까지 대기

# 데이터를 저장할 리스트
webtoons_data = []

try:
    # 모든 웹툰 항목을 가져오기 위한 XPath
    # 리스트 컨테이너를 먼저 찾고, 그 안의 모든 웹툰 항목을 선택합니다
    
    # 먼저 웹툰 리스트를 감싸는 컨테이너를 확인
    wait = WebDriverWait(driver, 10)
    container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'component_wrap')]")))
    
    # 해당 컨테이너 내의 모든 웹툰 항목을 선택
    webtoon_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'ComponentRankingChart__item--')]")
    
    # 만약 위 선택자로 찾을 수 없다면 다른 대안을 시도
    # if len(webtoon_items) == 0:
    # webtoon_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'component_wrap')]//li")
    
    # # 또 다른 대안
    # if len(webtoon_items) == 0:
    webtoon_items = driver.find_elements(By.XPATH, "//ul[contains(@class, 'ContentList')]//li")
    
    print(f"총 {len(webtoon_items)}개의 웹툰을 찾았습니다.")
    
    # 각 웹툰 요소에서 정보 추출
    for item in webtoon_items:
        try:
            # 썸네일 이미지 주소 추출
            thumbnail_img = item.find_element(By.XPATH, ".//img[contains(@class, 'Poster__image--')]")
            thumbnail_url = thumbnail_img.get_attribute('src') if thumbnail_img else 'N/A'
            
            # 타이틀 추출
            title_element = item.find_element(By.XPATH, ".//span[contains(@class, 'ContentTitle__title--')]")
            title = title_element.text if title_element else 'N/A'
            
            # 작가명 추출
            try:
                artist_elements = item.find_elements(By.XPATH, ".//a[contains(@class, 'ContentAuthor__author--')]")
                artists = []
                for artist_el in artist_elements:
                    artists.append(artist_el.text)
                artist = ', '.join(artists) if artists else 'N/A'
            except:
                artist = 'N/A'
            
            # 평점 추출
            try:
                rating_element = item.find_element(By.XPATH, ".//span[contains(@class, 'Rating__star_area--')]/span")
                rating = rating_element.text if rating_element else 'N/A'
            except:
                # 평점이 없는 경우를 처리
                rating = 'N/A'
            
            # 추출한 데이터 저장
            webtoons_data.append({
                '썸네일 이미지 주소': thumbnail_url,
                '타이틀': title,
                '작가명': artist,
                '평점': rating
            })
            
            print(f"웹툰 정보 추출: {title}")
            
        except Exception as e:
            print(f"웹툰 정보 추출 중 오류 발생: {e}")
    
    # 스크롤을 내려 더 많은 웹툰을 로드 (필요한 경우)
    if len(webtoons_data) < 10:  # 예상보다 적은 웹툰이 로드된 경우
        print("스크롤을 내려 더 많은 웹툰을 로드합니다...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 추가 콘텐츠 로드 대기
        
        # 추가로 로드된 웹툰 항목 찾기
        additional_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'ComponentRankingChart__item--')]")
        print(f"추가로 {len(additional_items) - len(webtoon_items)}개의 웹툰을 찾았습니다.")
        
        # 추가 항목 처리
        for item in additional_items[len(webtoon_items):]:
            try:
                thumbnail_img = item.find_element(By.XPATH, ".//img[contains(@class, 'Poster__image--')]")
                thumbnail_url = thumbnail_img.get_attribute('src') if thumbnail_img else 'N/A'
                
                title_element = item.find_element(By.XPATH, ".//span[contains(@class, 'ContentTitle__title--')]")
                title = title_element.text if title_element else 'N/A'
                
                try:
                    artist_elements = item.find_elements(By.XPATH, ".//a[contains(@class, 'ContentAuthor__author--')]")
                    artists = []
                    for artist_el in artist_elements:
                        artists.append(artist_el.text)
                    artist = ', '.join(artists) if artists else 'N/A'
                except:
                    artist = 'N/A'
                
                try:
                    rating_element = item.find_element(By.XPATH, ".//span[contains(@class, 'Rating__star_area--')]/span")
                    rating = rating_element.text if rating_element else 'N/A'
                except:
                    rating = 'N/A'
                
                webtoons_data.append({
                    '썸네일 이미지 주소': thumbnail_url,
                    '타이틀': title,
                    '작가명': artist,
                    '평점': rating
                })
                
                print(f"웹툰 정보 추출: {title}")
                
            except Exception as e:
                print(f"추가 웹툰 정보 추출 중 오류 발생: {e}")
    
except Exception as e:
    print(f"웹툰 목록 추출 중 오류 발생: {e}")

finally:
    # 웹 드라이버 종료
    driver.quit()

# 중복 항목 제거 (타이틀 기준)
unique_webtoons = []
unique_titles = set()
for webtoon in webtoons_data:
    if webtoon['타이틀'] not in unique_titles:
        unique_titles.add(webtoon['타이틀'])
        unique_webtoons.append(webtoon)

# 수집된 데이터 출력
print("\n=== 수집된 웹툰 정보 ===")
for i, webtoon in enumerate(unique_webtoons, 1):
    print(f"{i}. {webtoon['타이틀']} - {webtoon['작가명']} (평점: {webtoon['평점']})")

print(f"\n총 {len(unique_webtoons)}개의 웹툰 정보를 수집했습니다.")

# 데이터를 CSV 파일로 저장
if unique_webtoons:
    df = pd.DataFrame(unique_webtoons)
    df.to_csv('naver_monday_webtoons.csv', index=False, encoding='utf-8-sig')
    print("\n데이터를 'naver_monday_webtoons.csv' 파일로 저장했습니다.")
else:
    print("\n저장할 데이터가 없습니다.")
