from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime

from send_email import send_mail


def check_price(trigger_price):
    url = 'https://www.amazon.pl/kindle-paperwhite-8-gb-teraz-z-wyswietlaczem-68-i-regulowanym-podswietleniem-w-cieplym' \
          '-kolorze-bez-reklam/dp/B08N36XNTT?ref_=Oct_d_obs_d_22832468031&pd_rd_w=sQi6o&pf_rd_p=f3c0087e-c101-4b01-8657' \
          '-8ee971af1154&pf_rd_r=K1NS9EBCYZVVR61R9Y0P&pd_rd_r=3971854b-e53e-4a5e-b67d-909c3d1a0e39&pd_rd_wg=HqAgf' \
          '&pd_rd_i=B08N36XNTT '

    # from https://httpbin.org/get
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"}

    # connect to website

    page = requests.get(url, headers=headers)

    # picking data to scrape

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id='title').get_text()
    price = soup2.find(id='corePrice_feature_div', ).get_text('|', strip=True).split('|')[0].replace(',', '.')

    price = float(price.strip()[:-2])
    title = title.strip()
    today = datetime.date.today()
    title_simple = title.split(" ")[0]
    # building csv

    header = ['Title', 'Price', 'Date']
    data = [title, price, today]

    # appending data to csv

    with open('AmazonWebScraperOne.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    if price < trigger_price:
        send_mail(title_simple, trigger_price, url)


while True:
    check_price(500)
    time.sleep(86400)
