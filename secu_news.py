#pip install selenium
#pip install webdriver-manager
#Reference:https://liveyourit.tistory.com/40?category=872251
import sys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime

class CRAWL:

	def __init__(self):

		self.driver = ""
		self.news_url=""
		self.index=0

	# 크롤링을 시작할 뉴스 기사 URL 구성을 위해 index를 가져옴
	def parsing_news_url(self, url):

		chrome_options = Options()
		chrome_options.add_argument("--headless")  # Headless 모드로 설정
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
		self.driver.get(url)
		
		# 전체기사에서 첫 기사의 idx 가져오기
		depth_1=self.driver.find_element(By.ID, "scroll_up")
		depth_2=depth_1.find_element(By.TAG_NAME, "a")
		depth_3=depth_2.get_attribute("href")
		self.index = depth_3[44:50]
	
	
	def crawling(self):
	
		now = datetime.now()
		formattedDate = now.strftime("%Y%m%d")

		# 결과를 저장하기 위한 txt
		f = open('secunews_crawl_' + formattedDate + '.html', 'w', encoding='utf-8')
		
		for i in range(20):
			# 위에서 구한 index를 넣어 URL을 구성 (index는 계속 -1 됨)
			self.news_url = "https://www.boannews.com/media/view.asp?idx="+str(self.index)+"&page=1"
			print(self.news_url)
			
			# 강제 끊김을 방지하기 위한 sleep
			time.sleep(5)
			self.driver.get(self.news_url)
			
			# alert 경고창 처리를 위한 try, except 구문
			try:
				#is_alert = self.driver.switch_to_alert()     #셀레니움 이전 버전에서 동작하는 코드
				is_alert = self.driver.switch_to.alert
				is_alert.dismiss()
				self.index = int(self.index)
				self.index -= 1
			except:
				# 뉴스 기사 본문 텍스트에 접근
				news_title=self.driver.find_element(By.ID, "news_title02").text
				news_content=self.driver.find_element(By.ID, "news_content").text
				news_date=self.driver.find_element(By.ID, "news_util01").text
				news_date = news_date[10:20]
				
				# 출력
				#print("["+news_title+"]\n")
				#print(news_date+"\n")
				#print(news_content+"\n\n")
				
				# 파일에 쓰기
				f.write("<a href='" + self.news_url + "' target='_blank'>" + self.news_url + "</a><br/>")
				f.write("["+news_title+"]<br/>")
				f.write(news_date+"<br/>")
				f.write(news_content[0:100]+"...<br/>")
				f.write("-------------------------------------------------------------------------<br/><br/>")
				
				# 다음 기사 크롤링을 위해 index -1 을 해줌
				self.index = int(self.index)
				self.index -= 1
		
		f.close()
		self.driver.close()

	
if __name__=="__main__":
	
	# 보안뉴스 전체기사 URL
	secu_news_all = "https://www.boannews.com/media/t_list.asp"
	
	crawl = CRAWL()
	crawl.parsing_news_url(secu_news_all)
	crawl.crawling()