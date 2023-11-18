import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

url_Litres = "https://www.litres.ru/book/anita-shapira-326732/istoriya-izrailya-ot-istokov-sionistskogo-dvizheniya-69510613/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def webdriver_parse():
    service = Service(
        executable_path=r"D:\Projects\python\LotBook\tgbot\utiles\questions\firefox_driver\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", headers["User-Agent"])
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url=url_Litres)
        # Скролим до оглавления
        driver.execute_script("window.scrollTo(0, 40)")
        # Нажимаем на оглавление, чтобы получить список
        table_of_contents = driver.find_element(By.ID, "book_intro")
        table_of_contents.click()
        # Парсим оглавление
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result = soup.find("div", id="spoiler_popup").get_text()

        print(result)


        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def chekConnect():
    padge = requests.get(url_Litres, headers=headers)
    print(padge)

webdriver_parse()
