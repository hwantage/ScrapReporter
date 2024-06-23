import os
import requests
from datetime import datetime
import shutil

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
			"body": "@hwantage \n\n" + body1 + body2 + body3
		}
		response = requests.post(url, headers=headers, json=data)
		if response.status_code == 201:
			print("Issue created successfully")
			self.overwrite_txt_files(formattedDate)
		else:
			print("Failed to create issue. Status code:", response.status_code)
			print("Response content:", response.content.decode())

	def overwrite_txt_files(self, formattedDate):
		keyword_src = 'diff_keyword/' + formattedDate + '/'
		keyword_files = [f for f in os.listdir(keyword_src) if f.endswith('.txt')]
		for txt_file in keyword_files:
			shutil.move(os.path.join(keyword_src, txt_file), os.path.join('diff_keyword/', txt_file))

		changed_src = 'diff_changed/' + formattedDate + '/'
		changed_files = [f for f in os.listdir(changed_src) if f.endswith('.txt')]
		for txt_file in changed_files:
			shutil.move(os.path.join(changed_src, txt_file), os.path.join('diff_changed/', txt_file))
		print("Txt files moved successfully")            
			
if __name__=="__main__":
	
	issue = ISSUE()
	issue.create_issue()
