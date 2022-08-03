from abc import ABC, abstractmethod
import re
import time
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver

from .config import settings
from .exceptions import RequestException, ItemNotFound
from .item import Item


def _get_browser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent={settings.headers['User-Agent']}")
    driver = webdriver.Chrome(settings.webdriver, chrome_options=options)
    return driver

class Shop(ABC):
    @abstractmethod
    def get_items(self, request: str, items_count: int) -> List[Item]:
        raise NotImplemented

class ShopMvideo(Shop):
    main_url = "https://www.mvideo.ru"
    shop_name = 'МВидео'

    def get_items(self, request: str, items_count: int) -> List[Item]:
        url = f"{self.main_url}/product-list-page?q={'+'.join(request.split())}"
        browser = _get_browser()
        try:
            browser.get(url=url)
        except:
            raise RequestException
        height = browser.execute_script("return document.body.scrollHeight")
        for i in range(101):
            time.sleep(.1)
            browser.execute_script(f"window.scrollTo(0, {height * i / 100});")
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        items = []
        elements = soup.find_all("mvid-plp-product-picture")[:items_count]
        try:
            for element in elements:
                item = Item(
                    picture_url="https:" + \
                        element.find("picture").find("img", attrs={"class": ["product-picture__img", "product-picture__img--grid"]})["src"],
                    name=element.find_next("div", attrs={"class": ["product-card__title-line-container"]}).find("a").text.strip(),
                    price=int(
                        re.sub(
                            "[^0-9]+", 
                            "", 
                            element.find_next("div", attrs={"class": ["product-card__price-block-container"]}).find("span").text.strip(),
                            flags=re.IGNORECASE
                        )
                    ),
                    url=self.main_url + element.find("a", attrs={"class": ["product-picture-link"]})['href'],
                )
                items.append(item)
        except Exception as ex:
            print(ex)
        browser.quit()
        if len(items):
            return items
        raise ItemNotFound

class ShopSvyaznoy(Shop):
    main_url = "https://www.svyaznoy.ru"
    shop_name = 'Связной'

    def get_items(self, request: str, items_count: int) -> List[Item]:
        url = f"{self.main_url}/search?q={'+'.join(request.split())}"
        browser = _get_browser()
        try:
            browser.get(url=url)
        except:
            raise RequestException
        height = browser.execute_script("return document.body.scrollHeight")
        for i in range(101):
            time.sleep(.1)
            browser.execute_script(f"window.scrollTo(0, {height * i / 100});")
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        elements = soup.find_all("div", attrs={"data-key": re.compile("\d+")})
        items = []
        for element in elements[:items_count]:
            item = Item(
                picture_url=element.find("img", attrs={"itemprop": "image"})["src"],
                name=element.find("span", attrs={"itemprop": "name"}).text.strip(),
                price=int(
                    re.sub(
                        "[^0-9]+", 
                        "", 
                        element.find("span", attrs={"class": "b-product-block__visible-price"}).text.strip(),
                        flags=re.IGNORECASE
                    )
                ),
                url=self.main_url + element.find("a", attrs={"class": "b-product-block__main-link"})['href'],
            )
            items.append(item)
        browser.quit()
        if len(items):
            return items
        raise ItemNotFound

class ShopWildBerries(Shop):
    main_url = "https://www.wildberries.ru"
    shop_name = 'WILDBERRIES'

    def get_items(self, request: str, items_count: int) -> List[Item]:
        url = f"{self.main_url}/catalog/0/search.aspx?sort=popular&search={'+'.join(request.split())}"
        browser = _get_browser()
        try:
            browser.get(url=url)
        except:
            raise RequestException
        height = browser.execute_script("return document.body.scrollHeight")
        for i in range(101):
            time.sleep(.1)
            browser.execute_script(f"window.scrollTo(0, {height * i / 100});")
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        elements = soup.find_all("div", attrs={"id": re.compile("c\d+")})
        items = []
        for element in elements[:items_count]:
            item = Item(
                picture_url="https:" + element.find("img")["src"],
                name=element.find("span", attrs={"class": "goods-name"}).text.strip(),
                price=int(
                    re.sub(
                        "[^0-9]+", 
                        "", 
                        (element.find("ins", attrs={"class": "lower-price"}) or element.find("span", attrs={"class": "lower-price"})).text.strip(),
                        flags=re.IGNORECASE
                    )
                ),
                url=element.find("a")["href"],
            )
            items.append(item)
        browser.quit()
        if len(items):
            return items
        raise ItemNotFound

shops = {
    ShopMvideo.shop_name: ShopMvideo(),
    ShopSvyaznoy.shop_name: ShopSvyaznoy(),
    ShopWildBerries.shop_name: ShopWildBerries()
}