from bs4 import BeautifulSoup
import requests
#request library requests info from a website, like a real person going to a website and requesting information

standings_url = 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
data = requests.get(standings_url)

print(data)
soup = BeautifulSoup(data.text)
soup.select('table.stats_table')[0]
#jobs = soup.find_all('li', class_ = '')
