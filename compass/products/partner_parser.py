from bs4 import BeautifulSoup
import requests

def find_price_stolplit(SKU):
    "ищем название, цену и ссылку на товар по артиклю на сайте столплит"
    link = f'https://www.stolplit.ru/internet-magazin/search/?is_submit=Y&product_title={SKU}'
    HTML  = requests.get(link, stream=True)
    soup = BeautifulSoup(HTML.text, 'html.parser')
    offers = {}
    prices, names = soup.find_all("div",{'class':'product__price'}), soup.find_all("a",{'class':'js-product-link'})
    #print(''.join(link.get('href') for link in names))
    #print(names)
    clean_names = ([" ".join(name.text.replace('\n', '').split()) for name in names if name.text != 'Подробнее'])
    clean_prices = [float(price.find("span",{'class':'price'}).text.replace(' ', '')) for price in prices]
    clean_links = ['https://www.stolplit.ru'+link.get('href') for link in names if link.text == 'Подробнее']
    #print(clean_links)
    offers = dict(zip(clean_names, zip(clean_prices, clean_links)))
    return offers

