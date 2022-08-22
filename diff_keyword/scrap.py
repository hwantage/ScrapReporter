from urllib.request import Request, urlopen
import urllib.error
from bs4 import BeautifulSoup
from difflib import context_diff
import ssl
import os.path
from datetime import datetime

#안전하지 않은 연결 무시 NET::ERR_CERT_COMMON_NAME_INVALID
ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()
path = "C:/python/scraprepoter/diff_keyword/"

#데이터베이스 오픈
db = open(path + "db.txt", 'r', encoding='utf8')
matches = ["사업", "공고", "신규", "과제"]
report = ""
tempForSameTxtCheck = ""

def createFolder(directory):
    try:
         if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

now = datetime.now()
formattedDate = now.strftime("%Y%m%d")
createFolder(formattedDate)

while True:
    dbline = db.readline()
    if not dbline: break
    data = dbline.split(' ')
    name = data[0]
    url = data[1].replace("\n","")
    
    report += "\n<a href='" + url + "' target='_blank'>" + name + "</a>\n"

    try:
        req = Request(url)
        req.add_header('Cookie', 'JSESSIONID=43EnHJ1R1W26gIzDAxAFXnDLLn8C2dsCYOfdJ6yo.AP_msit_1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        result = urlopen(req).read()

    except urllib.error.HTTPError as e:
        print("HTTPError: {}".format(e.code))
        report += "HTTPError: {}".format(e.code) + "\n\n"
    except urllib.error.URLError as e:
        print("URLError: {}".format(e.reason))
        report += "URLError: {}".format(e.reason) + "\n\n"
    else:
        text = BeautifulSoup(result.decode('utf-8'), "html.parser")
        #스크랩된 내용 인코딩
        text_byte = text.encode('utf-8')
        
        file = path + name + ".txt"
        #기존 비교 대상 파일 있는지 확인
        #기존 파일이 있으면 새로운 파일로 저장하고 키워드 비교
        if os.path.isfile(file):
            file_new = path + formattedDate + "/" + name + ".txt"
            f = open(file_new,'w', encoding='utf8')
            f.write(text_byte.decode('utf-8'))
            #두 개의 파일 비교 시작
            with open(file, 'r', encoding='utf8') as f1:
                with open(file_new, 'r', encoding='utf8') as f2:
                    diff = context_diff(f1.readlines(), f2.readlines(), fromfile='f1', tofile='f2')
                    for line in diff:
                        if any(x in line for x in matches):
                            if line.startswith('+'):
                                soup = BeautifulSoup(line, "html.parser")
                                text = soup.get_text()
                                if len(text)>3:
                                    #중복 문자열이면 스킵
                                    if tempForSameTxtCheck != text.lstrip("+").strip():
                                        report += "+ " + text.lstrip("+").strip() + "\n\n"
                                        tempForSameTxtCheck = text.lstrip("+").strip()
	    
        #기존 파일이 없으면 신규 파일로 저장하고 자체 키워드 비교
        else:
            file = path + name + ".txt"
            f = open(file,'w', encoding='utf8')
            f.write(text_byte.decode('utf-8'))
            with open(file, 'r', encoding='utf8') as f1:
                for line in f1.readlines():
                    if any(x in line for x in matches):
                        soup = BeautifulSoup(line, "html.parser")
                        text = soup.get_text()
                        #print(text.lstrip("+").strip())
                        if len(text)>3:
                            report += "+ " + text.lstrip("+").strip() + "\n\n"
db.close()
print(report)
file = path + formattedDate + "/" + "report_keyword_" + formattedDate + ".html"
f = open(file,'w', encoding='utf8')
f.write(report.replace("\n","<br>"))
