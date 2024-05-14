import os
import requests
from datetime import datetime

class ISSUE:
	def create_issue(self):
		now = datetime.now()
		formattedDate = now.strftime("%Y%m%d")
		title = formattedDate + " news"
		body1 = open('secunews_crawl_' + formattedDate + '.html', 'r', encoding='utf-8').read()
		body2 = open('diff_keyword/' + formattedDate + '/report_keyword_' + formattedDate + '.html', 'r', encoding='utf-8').read()
		body3 = open('diff_changed/' + formattedDate + '/report_changed_' + formattedDate + '.html', 'r', encoding='utf-8').read()
		url = "https://api.github.com/repos/hwantage/ScrapReporter/issues"
		headers = {
			"Authorization": "token " + os.environ['ACTION_ACCESS_TOKEN'],
			"Accept": "application/vnd.github.v3+json"
		}

		data = {
			"title": title,
			"body": body1 + body2 + body3
		}
		response = requests.post(url, headers=headers, json=data)
		if response.status_code == 201:
			print("Issue created successfully")
		else:
			print("Failed to create issue. Status code:", response.status_code)
			
if __name__=="__main__":
	
	issue = ISSUE()
	issue.create_issue()
