import os
import execjs
import requests
import random
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

payload = {
    "fm-login-id": 'Lz429671594@outlook.com',
    'fm-login-password': 'pf52CE4JyGiY7fj'
}


def js_from_file(file_name):
    """
    reading javascript file
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()

    return result


js_code = execjs.compile(js_from_file(r"D:\App Development\Grabber\AliSliderCracker.js"))


def downloadSourceCode():
    store_id = int(input('Store ID to grab source from: '))
    numPages = int(input('Number of pages you want to scrape: '))
    path = input('The path you want to save the file: ')
    html_output_name = input('Name for html file: ')

    urls = []
    reqs = []

    for i in range(1, numPages + 1):
        urls.append("https://www.aliexpress.com/store/sale-items/" + str(store_id) + '/' + str(i) + ".html")

    for url in urls:
        req_result = requests.get(url, 'html.parser').text
        if 'pic-rind' not in req_result:
            js_code.call("bypass", url)
        else:
            reqs.append(req_result)

    with open(path + html_output_name + '.txt', 'w', encoding='gb18030', errors='ignore') as f:
        for req in reqs:
            f.write(req + "\n")
        f.close()


def getProductURL(list_dir):
    """
    :param list_dir:
    :return:
    """

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
            product_id = (url.split('.html')[0]).split('/item/')[1]
            with open("C://Users//Lenovo//Desktop//html//911651019//" + product_id + '.html', 'wb') as f:
                f.write(content)


if __name__ == '__main__':
    downloadSourceCode()
