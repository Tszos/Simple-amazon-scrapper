from bs4 import BeautifulSoup
import requests
import csv
import datetime

from src.config import URL, HEADERS
from src.send_email import send_mail


def check_price(trigger_price):
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='title').get_text()
    price = soup.find(id='corePrice_feature_div', ).get_text('|', strip=True).split('|')[0].replace(',', '.')
    price = float(price.strip()[:-2])
    title = title.strip()
    today = datetime.date.today()
    title_simple = title.split(" ")[0]
    data = [title, price, today]
    with open('AmazonWebScraperOne.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    if price < trigger_price:
        send_mail(title_simple, trigger_price, URL)