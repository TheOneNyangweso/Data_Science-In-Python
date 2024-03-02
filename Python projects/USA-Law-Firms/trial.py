from playwright.sync_api import sync_playwright
from parsel import Selector
import pandas as pd
import time

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "https://law.usnews.com/law-firms/millen-white-zelano-&-branigan-pc-6480", timeout=60000, wait_until='domcontentloaded')

    time.sleep(10)
    # get html
    html = page.content()
    # parse the HTML using parsel
    selector = Selector(text=html)

    name_of_law_firm = selector.xpath(
        '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/h1').extract_first(default=None)
    print(name_of_law_firm)

    time.sleep(10)
    # close the browser
    browser.close()
    pw.stop()
