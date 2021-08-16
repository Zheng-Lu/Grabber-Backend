import os
import re
import requests
import random
import json
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


AliExpress_headers = {
    'user-agent': random.choice(user_agent_list),
}

def downloadSourceCode(url):
    """

    :return:
    """
def getProductURL(list_dir):
    path = list_dir + '//'
    htmlDirEntries = sorted(
        [filename for filename in os.listdir(path) if filename.endswith(".html")])

    HTMLdict = {}
    for filename in htmlDirEntries:
        soup = BeautifulSoup(open(os.path.join(path, filename), encoding='gb18030', errors='ignore'), 'html.parser')
        HTMLdict[filename] = soup

    for filename in HTMLdict:
        HTMLdict[filename] = HTMLdict[filename].findAll('a', {'class': 'pic-rind'})
        for i in range(len(HTMLdict[filename])):
            HTMLdict[filename][i] = 'https:' + HTMLdict[filename][i].get('href')

    print(HTMLdict)
    return HTMLdict


def download_product(HTMLdict):
    for filename in HTMLdict:
        for url in HTMLdict[filename]:
            response = requests.get(url, headers=AliExpress_headers)
            content = response.content
            id = (url.split('.html')[0]).split('/item/')[1]
            with open("C://Users//Lenovo//Desktop//html//911651019//" + id + '.html', 'wb') as f:
                f.write(content)
