import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import unquote
import wget



try:
    if os.path.exists("source/homepage.html"):
        with open("source/homepage.html", "r") as f:
            html = f.read()
            print(html)
            soup = BeautifulSoup(html, "html.parser")
   
    else:
        url =  "https://github.com/swisskyrepo/PayloadsAllTheThings"
        r = requests.get(url)
        os.makedirs('source', exist_ok=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup)
        with open('source/homepage.html', 'w', encoding='utf-8') as f_out:
            f_out.write(str(soup))
except:
    print("Error: Could not connect to github")
    exit()

def download():
    for i in dic:
        # download_progress.set(value)
        url = dic[i].replace('/tree','')
        title = dic[i].split('/')[-1]
        title = title.replace(' ', '_')
        filepath = f'source/{title}_README.md'
        try:
            # print(f"{url}/README.md")
            if not os.path.exists(filepath):
                wget.download(f"{url}/README.md", out=filepath)
        except:
            try:
                if not os.path.exists(filepath):
                    wget.download(f"{url}/readme.md", out=filepath)
            except:
                pass

# create a directory name source with OS



ancs = soup.find_all('a')
# print(ancs)

filters = []
for i in range(len(ancs)):

    if '/swisskyrepo/PayloadsAllTheThings/tree/master/' in ancs[i].get('href'):
            filters.append(ancs[i])
# print(filters)
dic = {}
for i in range(len(filters)):
    dic[filters[i].text] = f"https://raw.githubusercontent.com{unquote(filters[i].get('href'))}"


dic.pop('.github')
print(dic)
download()