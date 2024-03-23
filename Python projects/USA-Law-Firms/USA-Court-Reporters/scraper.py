from playwright.sync_api import sync_playwright
from parsel import Selector
import pandas as pd
import csv
import time

INITIAL_URL = 'https://www.google.com/search?q=court+reporters+in+Iowa&sca_esv=d6727fb810734362&sca_upv=1&biw=1366&bih=683&tbm=lcl&ei=dKD-ZcK6Lq2E7NYPoOiD6Ag&udm=&ved=0ahUKEwjCxPbeiIqFAxUtAtsEHSD0AI0Q4dUDCAk&oq=court+reporters+in+Iowa&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhdjb3VydCByZXBvcnRlcnMgaW4gSW93YTIHEAAYgAQYEzIIEAAYFhgeGBMyChAAGBYYHhgPGBMyCBAAGBYYHhgTSNIJUABYAHAAeACQAQCYAY8CoAGPAqoBAzItMbgBDMgBAJgCAaACmQKYAwCIBgGSBwMyLTGgB6AD&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[43.4240669,-90.2266772],[41.1695636,-95.47927159999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:2'

STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming', 'Washington, D.C.'
]
TIMEOUT = 120000


def get_page_one(selector, state):
    for i in range(1, 21):
        index = str(i * 2)
        name = selector.xpath(
            f'html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        number = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()
        website = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/a/@href').get()
        print(name, number, state, website, sep='|')


def get_other_pages(selector, state):
    for i in range(1, 21):
        index = str(i * 2)
        name = selector.xpath(
            f'html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[1]/span/text()').get()
        if name is None:
            name = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[1]/span/text()').get()
        number = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/div/a/div/div/div[3]/text()').get()
        if number is None:
            number = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/div/a/div/div/div[3]/text()').get()
        website = selector.xpath(
            f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div[2]/div/a[1]/@href').get()
        if website is None:
            website = selector.xpath(
                f'/html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{index}]/div/div/a/@href').get()
        print(name, number, state, website, sep='|')


def scrape(state):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(INITIAL_URL, timeout=TIMEOUT,
                  wait_until='domcontentloaded')
        time.sleep(5)

        page.fill('//*[@id="APjFqb"]', f'court reporters in {state}')
        page.press('//*[@id="APjFqb"]', 'Enter')
        time.sleep(10)

        html = page.content()
        selector = Selector(text=html)

        get_page_one(selector=selector, state=state)

        while page.query_selector('//*[@id="pnnext"]'):
            page.click('//*[@id="pnnext"]')
            # Wait until the new content loads
            time.sleep(10)
            html = page.content()
            selector = Selector(text=html)
            print("I have the html!!\n")
            get_other_pages(selector=selector, state=state)
        else:
            print("no clickable element")
        print('done!!')

        browser.close()

        if state == state[-1]:
            pw.stop()


def run():
    for count, state in enumerate(STATES):
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
