# ScrapRepoter
키워드 기반 스크랩 및 DIFF 변경 사항 확인

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

python scrap.py

## 구조 및 설명

https://miro.com/app/board/uXjVO-otrNc=/?share_link_id=948596105654
