import requests
from bs4 import BeautifulSoup
import json
import csv

import selentiumParser


class myData:
    def __init__(self, name, price):
        self.name = name
        self.price = price

COOKIES = {}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
}

def getPage(url, pageNumber):
    pages = {
        "p": pageNumber,
    }
    response = requests.get(url, cookies=COOKIES, headers=HEADERS, params=pages)
    if response.status_code!=200:
        return "Error"
    dataHtml = response.json()['html']
    soup = BeautifulSoup(dataHtml, 'lxml')
    products = soup.find_all(class_ =  'catalog-product ui-button-widget')
    listId = []
    for product in products:
        listId.append(product.attrs['data-product'])
    return listId



def getPageCount(url):
    response = requests.get(url, cookies=COOKIES, headers=HEADERS)
    if response.status_code!=200:
        return 0
    dataHtml = response.json()['html']
    soup = BeautifulSoup(dataHtml, 'lxml')
    try:
        allPages = soup.find_all(class_='pagination-widget__page')
        lastPage = allPages[-1].attrs['data-page-number']
        return lastPage
    except:
        return 1


def getRespunceProduct(id):
    responseData = requests.get(f'https://www.dns-shop.ru/product/microdata/{id}/',
                                cookies=COOKIES, headers=HEADERS)
    if responseData.status_code==200:
        return responseData
    return "EROOR"


def getData(responseJson):
    name = responseJson['data']['name']
    price = responseJson['data']['offers']['price']
    data = myData(name, price)
    return data


def writeFile(data):
    with open('data.csv', 'w', encoding='UTF8') as file:
        fileWriter = csv.writer(file, delimiter=';')
        for name in data.keys():
            fileWriter.writerow([name, data[name]])


def main():
    print("Подготовка к работе...")
    JsId = selentiumParser.getJsID()
    if JsId == 'Error':
        print("Что то пошло не так...")
        return
    COOKIES['qrator_jsid'] = JsId
    url = 'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'
    data = {}
    print("Начало поиска товаров...")
    lastPage = int(getPageCount(url))
    if lastPage == 0:
        print("Что то пошло не так...")
        return
    for i in range(1,lastPage+1):
        print(f'Страница: {i}')
        listID = getPage(url,i)
        for id in listID:
            dataResponce = getRespunceProduct(id)
            jsonData = dataResponce.json()
            myData = getData(jsonData)
            print(f"{myData.name} ---- {myData.price}")
            data[myData.name] = myData.price
    print('Запись данных в файл...')
    writeFile(data)
    print('Готово')


if __name__=='__main__':
    main()


