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


js_code = execjs.compile(js_from_file("./AliSliderCracker.js"))


def downloadSourceCode():
    # store_id = int(input('Store ID to grab source from: '))
    numPages = int(input('Number of pages you want to scrape: '))

    urls = []
    requests_result = []

    for i in range(1, numPages + 1):
        urls.append("https://www.aliexpress.com/store/sale-items/" + str(store_id) + '/' + str(i) + ".html")

    for url in urls:
        req_result = requests.get(url, 'html.parser').text
        if 'pic-rind' not in req_result:
            js_code.call("bypass", url)
        else:
            requests_result.append(req_result)

    return requests_result


def readData():
    IDlist = []
    with open("productId.txt", "r") as f:
        for line in f:
            products = line.split(",")
            for product in products:
                IDlist.append(product.replace("'", ""))
    return IDlist


def downloadProductSrc(IDlist):
    urls_list = []

    for ID in IDlist:
        urls_list.append("https://www.aliexpress.com/item/" + ID + ".html")

    return urls_list


def getProductURL(requests_result):
    """
    :param requests_result:
    :return:
    """
    urls_list = []
    for srcPerPage in requests_result:
        soup = BeautifulSoup(srcPerPage, 'html.parser')
        urls_list.append(soup.findAll('a', {'class': 'pic-rind'}))

    for urls in urls_list:
        for i in range(len(urls)):
            urls[i] = 'https:' + urls[i].get('href')

    return urls_list


def download_product(urls_list):
    # Example of path: C://Users//Lenovo//Desktop//html//911651019//
    parent_dir = input("Enter the path you wanna store your HTML files: ")
    folder_name = str(store_id)
    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)

    for urls in urls_list:
        for url in urls:
            response = requests.get(url, headers=AliExpress_headers)
            content = response.content
            product_id = (url.split('.html')[0]).split('/item/')[1]
            file_name = product_id + '.html'
            with open(os.path.join(path, file_name), 'wb') as f:
                f.write(content)

    # for url in urls_list:
    #     try:
    #         response = requests.get(url, headers=AliExpress_headers)
    #         content = response.content
    #         product_id = (url.split('.html')[0]).split('/item/')[1]
    #         file_name = product_id + '.html'
    #         with open(os.path.join(path, file_name), 'wb') as f:
    #             f.write(content)
    #     except:
    #         js_code.call("bypass", url)


if __name__ == '__main__':
    store_id = int(input('Store ID to grab source from: '))
    # result1 = downloadSourceCode()
    # print(result1)
    # result2 = getProductURL(result1)
    # print(result2)
    # download_product(result2)

    url_list = downloadProductSrc(readData())
    download_product(url_list)
