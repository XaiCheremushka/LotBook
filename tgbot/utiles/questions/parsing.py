import time

import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# url_Litres = "https://www.litres.ru/book/uilyam-shirer/vzlet-i-padenie-tretego-reyha-19297129/"
url_Litres = "https://www.litres.ru/book/anita-shapira-326732/istoriya-izrailya-ot-istokov-sionistskogo-dvizheniya-69510613/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}





class OldPage:

    def create_content_sheet(self, html_code):
        print("content")
        soup = html_code

        result = []

        current_book = None
        current_chapter = None
        current_chapter_2 = None
        title = None

        for item in soup.find_all('div', style=re.compile(r'margin-left:(\d+)px;')):
            text = item.get_text(strip=True)

            # Определение, является ли элемент названием, книгой или главой
            # if 'margin-left:0px;' in item['style']:
            #     title = text
            if 'margin-left:20px;' in item['style']:
                current_book = text
                current_chapter = None
                current_chapter_2 = None
                result.append([current_book])
            elif 'margin-left:40px;' in item['style']:
                current_chapter = text
                current_chapter_2 = None
                result[-1].append([current_chapter])
            elif 'margin-left:60px;' in item['style']:
                current_chapter_2 = text
                result[-1][-1].append([current_chapter_2])

        return result


    def parse_info(self, html_code):
        print("info")
        info = {
            "title": html_code.find('h1', itemprop="name").get_text(),
            "autor": html_code.find('div', class_="biblio_book_author").get_text()[6:],
            "ISBN": html_code.select_one('div.biblio_book_info_detailed_right dd').get_text(),
            "total_pages": re.findall(r'\d+', html_code.find('li', class_="volume").get_text())[0],
            "date_of_publication": html_code.select_one(
                'div.biblio_book_info_detailed_left dd:nth-of-type(2)') if html_code.select_one(
                'div.biblio_book_info_detailed_left dt:nth-of-type(2)').get_text() in ["Дата перевода:",
                                                                                       "Дата написания:"] else html_code.select_one(
                'div.biblio_book_info_detailed_left dd:nth-of-type(3)')
        }

        return info

    def webdriver_parse(self, url, driver):

            driver.get(url=url)
            # Скролим до оглавления
            driver.execute_script("window.scrollTo(0, 200)")
            # Нажимаем на оглавление, чтобы получить список
            table_of_contents = driver.find_element(By.ID, "book_intro")

            if table_of_contents is not None:
                table_of_contents.click()
            else:
                print("Элемент не найден")
            # Парсим оглавление
            soup = BeautifulSoup(driver.page_source, "html.parser")
            info = self.parse_info(soup)
            result = soup.find("div", id="spoiler_popup")
            content_sheet = self.create_content_sheet(result)

            for r in content_sheet:
                print(r)

            return content_sheet, info


class NewPage:

    def create_content_sheet(self, html_code):
        print("content")
        soup = html_code

        result = []

        for item in soup.find_all('div'):
            if not bool(item.attrs):
                pass
            elif item["class"] == "BookTableContent-module__chapter_firstDeep_3oO5D":
                result.append([item.get_text()])
            elif item["class"] == "BookTableContent-module__chapter_secondDeep_2RGMm":
                result[-1].append([item.get_text()])
            else:
                result[-1][-1].append([item.get_text()])

        return result


    def parse_info(self, html_code):
        print("info")
        info = {
            "title": html_code.find('h1', itemprop="name").get_text(),
            "autor": html_code.select_one('div.Truncate__truncated_2nRnu > span').get_text(),
            "date_of_publication": None,
            "total_pages": None,
            "ISBN": None
        }

        characteristics = html_code.find_all('div', class_="CharacteristicsBlock-module__characteristic_2SKY6")
        for character in characteristics:
            print(character.find('div', class_='CharacteristicsBlock-module__characteristic__title_3_QiC').get_text())

            match character.find('div', class_='CharacteristicsBlock-module__characteristic__title_3_QiC').get_text():
                case "Дата перевода: ":
                    print(character.find_all('span')[1])
                    info["date_of_publication"] = character.find_all('span')[1].get_text()
                case "Объем: ":
                    info["total_pages"] = re.findall(r'\d+', character.find_all('span')[1].get_text())[0]
                case "ISBN: ":
                    info["ISBN"] = character.find_all('span')[1].get_text()

        return info

    def webdriver_parse(self, url, driver):

            driver.get(url=url)
            # Скролим до оглавления
            # driver.execute_script("window.scrollTo(0, 4500)")
            # Нажимаем на оглавление, чтобы получить список
            table_of_contents = driver.find_element(By.XPATH,
                                                    "//div[@class='FunctionalButton-module__funcButtonContent_-igzJ BookTableContent-module__buttonTableContentWrapper_1mydD']")
            table_of_contents.click()
            # Парсим оглавление
            soup = BeautifulSoup(driver.page_source, "html.parser")
            info = self.parse_info(soup)
            result = soup.find("div", class_="BookTableContent-module__bookTableContent_cOJ8T")
            content_sheet = self.create_content_sheet(result)

            for r in content_sheet:
                print(r)

            return content_sheet, info


def parse(url: str):
    service = Service(
        executable_path=r"D:\Projects\python\LotBook\tgbot\utiles\questions\firefox_driver\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", headers["User-Agent"])
    driver = webdriver.Firefox(service=service, options=options)

    try:
        page = NewPage()
        content_sheet, info = page.webdriver_parse(url, driver)
        print("Успешно распашена новая страница!")
        print("Оглавление")
        print(item for item in content_sheet)
        print("Остальная информация")
        print(item for item in info)

    except Exception as ex:
        print(ex)
        try:
            page = OldPage()
            content_sheet, info = page.webdriver_parse(url, driver)
            print("Успешно распашена старая страница!")
            print("Оглавление")
            print(item for item in content_sheet)
            print("Остальная информация")
            print(item for item in info)
        except Exception as ex:
            print(ex)
            print("Ошибка. Проверьте есть ли на этой странице оглавление и остальная информация о книге"
                  "корректна. На странице должны присутствовать: 'Оглавление', 'Автор', 'Объем', 'Дата перевода' или "
                  "'Дата написания', а также ISBN.")
    finally:
        driver.close()
        driver.quit()





    # Проверить URL на наличие audiobook, не парсить если оно есть.



parse(url_Litres)

# padge = requests.get(url_Litres, headers=headers)
# soup = BeautifulSoup(padge.text, "html.parser")
# print(parse_info(soup))