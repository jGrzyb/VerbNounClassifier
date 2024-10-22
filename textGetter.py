import requests
from bs4 import BeautifulSoup

url = 'https://sacred-texts.com/bib/wb/esp/index.htm'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all(['a'])[6:]
    links = [l for l in links if 'href' in l.attrs]

    book = ''
    for i, l in enumerate(links):
        u = 'https://sacred-texts.com/bib/wb/esp/' + l['href']
        print(f'{u}')
        resp = requests.get(u)
        if resp.status_code == 200:
            chapterSoup = BeautifulSoup(resp.content, 'html.parser')
            paragraphs = chapterSoup.find_all('p')
            for p in paragraphs:
                text = p.text.strip()
                annotations = p.find('a')
                if 'name' in annotations.attrs:
                    annotations = annotations['name'][3:]
                    text = text.replace(annotations, '') + "\n"
                    book += text
                    
    with open('text.txt', 'w') as file:
        file.write(book)