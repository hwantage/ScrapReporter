# ScrapRepoter
키워드 기반 스크랩 및 DIFF 변경 사항 확인

/diff_keyword/db.txt 파일에 명시된 url의 변경사항을 키워드 기반으로 확인

/diff_changed/db.txt 파일에 명시된 url의 변경사항을 diff 기반으로 확인

https://www.boannews.com 의 보안 카테고리 뉴스 수집

## GIT 연동
git init

git add ./diff_changed/scrap.py
git add ./diff_changed/db.txt
git add ./diff_keyword/scrap.py
git add ./diff_keyword/db.txt

git commit -m 'First Commit'

git remote add origin https://github.com/hwantage/ScrapRepoter.git

git push -u origin master

## 실행 방법

python ./diff_keyword/scrap.py

python ./diff_changed/scrap.py

python ./secu_news.py

## 구조 및 설명

https://miro.com/app/board/uXjVOmAO96A=/?share_link_id=344142157749
