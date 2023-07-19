from bs4 import BeautifulSoup
import requests
parts = ('сл-40','ас-44', 'ас-45', 'ас-46', 'ас-47','ас-48')

for part in parts:
        
    link = f'https://www.stolplit.ru/internet-magazin/search/?is_submit=Y&product_title={part}'
    headers = {'user-agent': 'my-app/0.0.1'}

    HTML  = requests.get(link, stream=True)
    soup = BeautifulSoup(HTML.text, 'html.parser')
    offers = {}
    offers[]
    prices, names = soup.find_all("div",{'class':'product__price'}), soup.find_all("div",{'class':'product__info'})
    for price in prices:
        text = price.find("span",{'class':'price'}).text
        print(f'{part}: {text}')