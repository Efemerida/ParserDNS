import os
import time
from platform import system

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def getCookie():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-plugins-discovery")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")

    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
      '''
    })

    driver.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/')
    time.sleep(1)
    data = driver.get_cookies()
    driver.quit()
    return data


def getJsID():
    cookie = getCookie()
    for cook in cookie:
        if cook.get('name') == 'qrator_jsid':
            return cook.get('value')
    return 'Error'


if __name__=='__main__':
    getJsID()