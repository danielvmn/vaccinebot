from telegram import Bot
from bs4 import BeautifulSoup
from decouple import config, Csv
from telegram import Bot
import logging
import requests
import re
import time

# Environment settings (Telegram chat id / API token)
telegramToken = config('token')
mainGroupid = config('main_group')
bot = Bot(token=telegramToken)

# Logging setup
format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=format, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def getUpdate():
    url = 'https://www.prullenbakvaccin.nl/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    available = soup.findAll(text=re.compile('Ga enkel naar de praktijk'))
    if available:
        total = soup.find('div', {'id': 'locations-container'}).find('h5').get_text()
        total3 = [line for line in total.split('\n') if line.strip() != '']
        return(" ".join(total3))


available = getUpdate()
if available:
    bot.send_message(chat_id=mainGroupid, text=available)

while True:
    newData = getUpdate()
    if newData and newData != available:
        available = newData
        bot.send_message(chat_id=mainGroupid, text=available)
        logging.info(f'Site updated, sending message to the group.')
    else:
        logging.info(f'Site not updated, waiting 60 seconds.')
    time.sleep(60)

