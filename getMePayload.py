import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import unquote


url =  "https://github.com/swisskyrepo/PayloadsAllTheThings"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# create a directory name source with OS
os.makedirs('source', exist_ok=True)

with open('source/homepage.html', 'w', encoding='utf-8') as f_out:
    f_out.write(soup.prettify())

ancs = soup.find_all('a')

filters = []
for i in range(len(ancs)):

    if '/swisskyrepo/PayloadsAllTheThings/tree/master/' in ancs[i].get('href'):
            filters.append(ancs[i])

dic = {}
for i in range(len(filters)):
    dic[filters[i].text] = f"https://raw.githubusercontent.com{unquote(filters[i].get('href'))}"

dic.pop('.github')
print(dic)