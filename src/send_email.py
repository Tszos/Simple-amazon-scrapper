import os
import smtplib

login = os.environ.get("TSZOS_EMAIL")
password = os.environ.get("TSZOS_PASSWORD")


def send_mail(item, price, url):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(login, password)

    subject = f'cena {item} spadla ponizej {price} zl'
    body = f'teraz mozna kupic taniej. Link: {url}'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(login, login, msg)
