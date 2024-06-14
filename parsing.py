import requests
from bs4 import BeautifulSoup
import csv
import time
from random import randint

file = open("product.csv", "w", encoding="utf-8-sig", newline="\n")
write_obj = csv.writer(file)
write_obj.writerow(["title", "price"])

base_url = 'https://www.domino.com.ge/products/tools/page-'
num_pages = 5

for page in range(1, num_pages + 1):
    url = f'{base_url}{page}/'
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    section = soup.find('div', class_='grid-list')

    products = section.find_all('div', class_='ty-column3')

    for product in products:
        information = product.find('div', class_='ut2-gl__name')
        title = information.a.text.strip()
        print(title)

        prices = product.find('span', class_='ty-price')
        price = prices.text.strip()
        print(price)
        write_obj.writerow([title, price])
    time.sleep(randint(5, 10))
