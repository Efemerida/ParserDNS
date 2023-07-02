import requests
from bs4 import BeautifulSoup
import json
import csv


class myData:
    def __init__(self, name, price):
        self.name = name
        self.price = price

COOKIES = {
    'current_path': '605bfdc517d7e9e23947448a9bf1ce16ac36b884434a3fdb10db053793c50392a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22city%22%3A%2230b7c1f3-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D',
    'phonesIdent': 'abef75e78bba31456efd84c288def09b3bfecd3ca29210ef53e0a624cb980963a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22b720c1b2-fe71-4545-987d-89e232e1b1ce%22%3B%7D',
    'cartUserCookieIdent_v3': '09b5832c3193fd8bcc9d978aecd343f3e3dd0c79d14dbba5cfa78174927e2990a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22f91e0c49-be19-3db1-b13a-dc6b29f4c91a%22%3B%7D',
    'PHPSESSID': 'b8e6b8be1299a141d30ca9e05bfbdd96',
    '_gcl_au': '1.1.2125823669.1688108716',
    '_ga_FLS4JETDHW': 'GS1.1.1688305691.4.1.1688305902.60.0.0',
    '_ga': 'GA1.2.146616522.1688108716',
    'tmr_lvid': 'b12fe4db2be11f93f4a5288f39006e8a',
    'tmr_lvidTS': '1688108717112',
    '_ym_uid': '1688108717669222099',
    '_ym_d': '1688108718',
    'rrpvid': '864755800871860',
    'rcuid': '649e7eb7cd4bf376203079d6',
    '_gid': 'GA1.2.177670721.1688224501',
    'tmr_detect': '0%7C1688305714207',
    'qrator_jsr': '1688305688.984.qEEq9xYJcFelkjtb-te1cjsqafv5fcej8jubq2ugoprcms15g-00',
    'qrator_ssid': '1688305689.134.7xQqGrBj2YFuVKkl-95cnbcchmt49k5630fa8f0v27m8jaf5q',
    'qrator_jsid': '1688305688.984.qEEq9xYJcFelkjtb-7l68jtrkskplmmc3brere5hvlaav8odl',
    'lang': 'ru',
    '_csrf': '13161da611b6e299258bb6c3051f267d6e692f13f8248ad316fdebdafe3a62a5a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22iBPcJo6wY19wLu4FCjkK5JwP6wPLgQSd%22%3B%7D',
    'city_path': 'moscow',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'rr-testCookie': 'testvalue',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'multipart/form-data; boundary=---------------------------84470547712199249893080158300',
    'Referer': 'https://www.dns-shop.ru/catalog/17a9de8616404e77/igry-dlya-pk/no-referrer',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRF-Token': 'qzREN3QbpQxF1rFtIY531jDklBrK0pIBgdnAXcxBzLjCdhRUPnSTexzniBpt-0OQc47_Uf-Y5VG3rpARqxCf3A==',
    'Origin': 'https://www.dns-shop.ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    # 'Cookie': 'current_path=605bfdc517d7e9e23947448a9bf1ce16ac36b884434a3fdb10db053793c50392a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22city%22%3A%2230b7c1f3-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; phonesIdent=abef75e78bba31456efd84c288def09b3bfecd3ca29210ef53e0a624cb980963a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22b720c1b2-fe71-4545-987d-89e232e1b1ce%22%3B%7D; cartUserCookieIdent_v3=09b5832c3193fd8bcc9d978aecd343f3e3dd0c79d14dbba5cfa78174927e2990a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22f91e0c49-be19-3db1-b13a-dc6b29f4c91a%22%3B%7D; PHPSESSID=b8e6b8be1299a141d30ca9e05bfbdd96; _gcl_au=1.1.2125823669.1688108716; _ga_FLS4JETDHW=GS1.1.1688305691.4.0.1688305706.45.0.0; _ga=GA1.2.146616522.1688108716; tmr_lvid=b12fe4db2be11f93f4a5288f39006e8a; tmr_lvidTS=1688108717112; _ym_uid=1688108717669222099; _ym_d=1688108718; rrpvid=864755800871860; rcuid=649e7eb7cd4bf376203079d6; _gid=GA1.2.177670721.1688224501; tmr_detect=0%7C1688305696557; qrator_jsr=1688305688.984.qEEq9xYJcFelkjtb-te1cjsqafv5fcej8jubq2ugoprcms15g-00; qrator_ssid=1688305689.134.7xQqGrBj2YFuVKkl-95cnbcchmt49k5630fa8f0v27m8jaf5q; qrator_jsid=1688305688.984.qEEq9xYJcFelkjtb-7l68jtrkskplmmc3brere5hvlaav8odl; lang=ru; _csrf=13161da611b6e299258bb6c3051f267d6e692f13f8248ad316fdebdafe3a62a5a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22iBPcJo6wY19wLu4FCjkK5JwP6wPLgQSd%22%3B%7D; city_path=moscow; _gat=1; _gat_%5Bobject%20Object%5D=1; _gat_UA-8349380-2=1; _ym_isad=2; _ym_visorc=b; rr-testCookie=testvalue',
}

def getPage(url, pageNumber):
    pages = {
        "p": pageNumber,
    }
    response = requests.get(url, cookies=COOKIES, headers=HEADERS, params=pages)
    dataHtml = response.json()['html']
    soup = BeautifulSoup(dataHtml, 'lxml')
    products = soup.find_all(class_ =  'catalog-product ui-button-widget')
    listId = []
    for product in products:
        listId.append(product.attrs['data-product'])
    return listId



def getPageCount(url):
    response = requests.get(url, cookies=COOKIES, headers=HEADERS)
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
    return responseData


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
    url = 'https://www.dns-shop.ru/catalog/17a9de8616404e77/igry-dlya-pk/'
    data = {}
    print("Начало поиска товаров...")
    lastPage = int(getPageCount(url))
    for i in range(1,lastPage+1):
        print(f'Страница: {i}')
        listID = getPage(url,i)
        for id in listID:
            jsonData = getRespunceProduct(id).json()
            myData = getData(jsonData)
            print(f"{myData.name} ---- {myData.price}")
            data[myData.name] = myData.price
    print('Запись данных в файл...')
    writeFile(data)
    print('Все прошло успешно')


if __name__=='__main__':
    main()

