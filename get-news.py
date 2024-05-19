from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import pandas as pd
import os
import sys

current_dir = os.getcwd()
path = os.path.join(current_dir, "chromewebdriver", "chromedriver.exe")
print(path)

now = datetime.now()
date_string = now.strftime("%d%m%Y")

web_site = "https://www.thesun.co.uk/sport/football/"


service = Service(executable_path=path)
options = Options()
options.add_argument('ignore-certificate-errors')

# Headless mode
options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=options)

driver.get(web_site)

container_links = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]/a')
container_titles = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]/a/span')
container_subtitles = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]/a/h3')
container_descriptions = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]/a/p')

links = []
for link in container_links:
    links.append(link.get_attribute('href'))
titles = []
for title in container_titles:
    titles.append(title.text)
subtitles = []
for subtitle in container_subtitles:
    subtitles.append(subtitle.text)

data = {
    'Title': titles,
    'Subtitle': subtitles,
    'Link': links
}
df = pd.DataFrame(data)
file_output = os.path.join(current_dir, f'news-{date_string}.csv')
df.to_csv(file_output, encoding='utf-8')

driver.quit()
