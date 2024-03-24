# This script handles all the edge cases that is not related to the main task.
# There'll be a lot of modification when handling edge cases that is why
# I decided to put it in separate file instead of adding them into main code in scraper.py
from playwright.sync_api import sync_playwright
from parsel import Selector
import pandas as pd
import csv
import time

INITIAL_URL = 'https://www.google.com/search?q=court+reporters+in+Iowa&sca_esv=d6727fb810734362&sca_upv=1&biw=1366&bih=683&tbm=lcl&ei=dKD-ZcK6Lq2E7NYPoOiD6Ag&udm=&ved=0ahUKEwjCxPbeiIqFAxUtAtsEHSD0AI0Q4dUDCAk&oq=court+reporters+in+Iowa&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhdjb3VydCByZXBvcnRlcnMgaW4gSW93YTIHEAAYgAQYEzIIEAAYFhgeGBMyChAAGBYYHhgPGBMyCBAAGBYYHhgTSNIJUABYAHAAeACQAQCYAY8CoAGPAqoBAzItMbgBDMgBAJgCAaACmQKYAwCIBgGSBwMyLTGgB6AD&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[43.4240669,-90.2266772],[41.1695636,-95.47927159999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:2'

TIMEOUT = 120000

edge_states = ['Colorado', 'Alaska', 'Hawaii', 'Massachusetts',
               'Maine', 'New Mexico', 'Texas', 'Vermont', 'Washington']


def get_other_pages(selector, edge_state):
    for i in range(1, 21):
        index = str(i * 2)
        current_state = edge_state

        name = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()

        number = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()

        website = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/a/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/a/@href').get()
        print(name, number, current_state, website, sep='|')


def get_page_one(selector, edge_state):
    for i in range(1, 21):
        index = str(i * 2)
        name = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()

        number = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()

        website = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/a/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[4]/div[{index}]/div/div/a/@href').get()

        current_state = edge_state

        print(name, number, current_state, website, sep='|')


def scrape(state):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(INITIAL_URL, timeout=TIMEOUT,
                  wait_until='domcontentloaded')
        time.sleep(5)

        page.fill('//*[@id="APjFqb"]', f'court reporters in {state}')
        page.press('//*[@id="APjFqb"]', 'Enter')
        time.sleep(20)

        html = page.content()
        selector = Selector(text=html)

        get_page_one(selector=selector, edge_state=state)

        while page.query_selector('//*[@id="pnnext"]'):
            page.click('//*[@id="pnnext"]')
            # Wait until the new content loads
            time.sleep(20)
            html = page.content()
            selector = Selector(text=html)
            print("I have the html!!\n")
            get_other_pages(selector=selector, edge_state=state)
        else:
            print("no clickable element")
        print('done!!')


def run():
    for count, state in enumerate(edge_states):
        try:
            scrape(state=state)
            print(f'State of {state} data scraped successfully')
        except:
            with open("error_log.txt", 'a') as f:
                f.write(
                    str(f'Iteration {count} for the state of {state} has some errror\n'))
            continue
        time.sleep(30)
    print(f"Scraped ALL states")


if __name__ == '__main__':
    run()
