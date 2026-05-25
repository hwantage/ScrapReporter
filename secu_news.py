import sys
import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

class CRAWL:
    def __init__(self):
        self.news_url = ""
        self.index = 0

        # 1. CI/CD 컨테이너 환경 최적화 옵션 (메모리 부족 및 렌더링 지연 방지)
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # 최신 헤드리스 모드
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        
        # 2. WebDriver 초기화 및 전역 타임아웃 설정
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.set_page_load_timeout(30) # 응답 지연 시 30초 후 TimeoutException 발생

    def parsing_news_url(self, url):
        try:
            self.driver.get(url)
            
            # 전체기사에서 첫 기사의 idx 가져오기
            depth_1 = self.driver.find_element(By.ID, "scroll_up")
            depth_2 = depth_1.find_element(By.TAG_NAME, "a")
            depth_3 = depth_2.get_attribute("href")
            
            # 3. 불안정한 하드코딩 인덱스 슬라이싱(depth_3[44:50])을 안전한 파싱으로 변경
            if "idx=" in depth_3:
                extracted_idx = depth_3.split("idx=")[1].split("&")[0]
                self.index = int(extracted_idx)
                print(f"[INFO] Target Start Index: {self.index}")
            else:
                raise ValueError("URL에서 'idx=' 값을 찾을 수 없습니다.")
                
        except TimeoutException:
            print(f"[ERROR] 메인 페이지 로드 타임아웃: {url}", file=sys.stderr)
            self.driver.quit()
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] 최신 기사 인덱스 확보 실패: {e}", file=sys.stderr)
            self.driver.quit()
            sys.exit(1)
    
    def crawling(self):
        formattedDate = datetime.now().strftime("%Y%m%d")
        
        # 4. 컨텍스트 매니저(with)를 사용하여 파일 I/O 안전성 확보
        with open(f'secunews_crawl_{formattedDate}.html', 'w', encoding='utf-8') as f:
            for i in range(20):
                self.news_url = f"https://www.boannews.com/media/view.asp?idx={self.index}&page=1"
                print(f"[INFO] Crawling ({i+1}/20): {self.news_url}")
                
                try:
                    self.driver.get(self.news_url)
                    time.sleep(3) # 서버 과부하 방지 및 렌더링 딜레이 확보
                    
                    # 5. Alert 처리 로직 개선 (범용 Exception 대신 명시적 Exception 사용)
                    try:
                        is_alert = self.driver.switch_to.alert
                        is_alert.dismiss()
                        print(f"[WARN] Alert detected and dismissed at index {self.index}")
                        self.index -= 1
                        continue # 기사가 삭제되었거나 권한이 없는 경우 다음 기사로 스킵
                    except NoAlertPresentException:
                        pass # 알림창이 없으면 정상 진행

                    # 뉴스 기사 본문 텍스트 추출
                    news_title = self.driver.find_element(By.ID, "news_title02").text
                    news_content = self.driver.find_element(By.ID, "news_content").text
                    news_date_raw = self.driver.find_element(By.ID, "news_util01").text
                    news_date = news_date_raw[10:20]
                    
                    # 파일 쓰기 (f-string 적용하여 가독성 개선)
                    f.write(f"<a href='{self.news_url}' target='_blank'>{self.news_url}</a><br/>\n")
                    f.write(f"[{news_title}]<br/>\n")
                    f.write(f"{news_date}<br/>\n")
                    f.write(f"{news_content[0:100]}...<br/>\n")
                    f.write("-------------------------------------------------------------------------<br/><br/>\n")
                    
                except TimeoutException:
                    print(f"[WARN] 페이지 로드 타임아웃, 다음 기사로 스킵합니다: {self.news_url}")
                except Exception as e:
                    print(f"[WARN] 데이터 파싱 실패, 다음 기사로 스킵합니다: {e}")
                
                # 다음 기사 크롤링을 위해 index 감소
                self.index -= 1
        
        # 6. 드라이버 완전 종료 (close가 아닌 quit 사용)
        self.driver.quit()

if __name__ == "__main__":
    secu_news_all = "https://www.boannews.com/media/t_list.asp"
    
    crawl = CRAWL()
    crawl.parsing_news_url(secu_news_all)
    crawl.crawling()
