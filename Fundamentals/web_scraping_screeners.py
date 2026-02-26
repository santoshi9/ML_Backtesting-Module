import urllib3
from  bs4 import BeautifulSoup
http = urllib3.PoolManager()
url = 'https://www.screener.in/company/RELIANCE/consolidated/'
response = http.request('GET', url)
output = response.data
soup = BeautifulSoup(output, 'html.parser')
company_ratios = soup.find_all('div', class_='company-ratios')
read_table = company_ratios[0].find_all('tr')
print(read_table)
# print(soup.prettify())