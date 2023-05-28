import requests
from bs4 import BeautifulSoup

spec = input("Enter language by which you want see statistics of used technologies >> ")
techs = open("technologies", "r").read().split(',')
techs_counter = {}
try:
    html_text = requests.get(f'https://djinni.co/jobs/?all-keywords=&any-of-keywords=&exclude-keywords=&primary_keyword={spec}').text
    soup = BeautifulSoup(html_text, 'lxml')
    last_page = int(soup.find_all('li', class_="page-item")[-2].text)
    text_cards = []

    for i in range(1, last_page):
        html_text = requests.get(f'https://djinni.co/jobs/?all-keywords=&any-of-keywords=&exclude-keywords=&primary_keyword={spec}&page={i}').text
        soup = BeautifulSoup(html_text, 'lxml')
        text_cards += soup.find_all('div', class_="text-card truncated overflow-hidden mw-100 mb-1 js-show-more")

    for i in range(len(text_cards)):
        for tech in techs:
            if tech.lower() in text_cards[i].text.lower():
                if tech in techs_counter:
                    techs_counter[tech] += 1
                else:
                    techs_counter[tech] = 1

    techs_counter = dict(sorted(techs_counter.items(), key=lambda item: item[1], reverse=True))

    print(f"Total amount of vacancies: {len(text_cards)}")
    for k in techs_counter:
        print(f"{k}: {techs_counter[k]}")
except IndexError:
    print('Unfortunately there is no job opportunities with this technology.')
