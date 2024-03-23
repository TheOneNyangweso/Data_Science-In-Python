from playwright.sync_api import sync_playwright
from parsel import Selector
import pandas as pd
import csv
import time

url = 'https://www.google.com/search?q=court+reporters+in+Iowa&sca_esv=d6727fb810734362&sca_upv=1&biw=1366&bih=683&tbm=lcl&ei=dKD-ZcK6Lq2E7NYPoOiD6Ag&udm=&ved=0ahUKEwjCxPbeiIqFAxUtAtsEHSD0AI0Q4dUDCAk&oq=court+reporters+in+Iowa&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhdjb3VydCByZXBvcnRlcnMgaW4gSW93YTIHEAAYgAQYEzIIEAAYFhgeGBMyChAAGBYYHhgPGBMyCBAAGBYYHhgTSNIJUABYAHAAeACQAQCYAY8CoAGPAqoBAzItMbgBDMgBAJgCAaACmQKYAwCIBgGSBwMyLTGgB6AD&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[43.4240669,-90.2266772],[41.1695636,-95.47927159999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:2'
new_url = 'https://www.google.com/search?q=court+reporters+in+wisconsin&sca_esv=d6727fb810734362&sca_upv=1&biw=1366&bih=683&tbm=lcl&ei=dKv-ZdjbFJC9xc8P2quWoA4&udm=&oq=court+reporters+in+w&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhRjb3VydCByZXBvcnRlcnMgaW4gdyoCCAIyBxAAGIAEGBMyBxAAGIAEGBMyBxAAGIAEGBMyBxAAGIAEGBMyCBAAGBYYHhgTMggQABgWGB4YEzIIEAAYFhgeGBMyCBAAGBYYHhgTMggQABgWGB4YEzIKEAAYFhgeGA8YE0j8LFDCCVjMG3ADeACQAQCYAdkCoAGOC6oBBTItMy4yuAEByAEA-AEBmAIIoALdC8ICBRAhGKABmAMAiAYBkgcHMy4wLjMuMqAHnRE&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[45.077770199999996,-87.4862903],[42.9191466,-91.7219049]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:2'
TIMEOUT = 120000


def scraper():
    with sync_playwright() as pw:
        try:
            browser = pw.firefox.launch(headless=False)
            page = browser.new_page()

            page.goto(new_url, timeout=TIMEOUT, wait_until='domcontentloaded')
            time.sleep(5)

            html = page.content()
            selector = Selector(text=html)

            page.fill('//*[@id="APjFqb"]', f'court reporters in Alabama')

            time.sleep(5)
            page.press('//*[@id="APjFqb"]', 'Enter')
            time.sleep(5)
            print('DONE!!!')

            while page.query_selector('//*[@id="pnnext"]'):
                page.click('//*[@id="pnnext"]')
                # Wait until the new content loads
                time.sleep(10)
                html = page.content()
                selector = Selector(text=html)
                print("I have the html!!\n")

            else:
                print("no clickable element")

            print('done!!')

        except Exception as e:
            with open("error_log.txt", 'a') as f:
                f.write(str(f'failed to access webpage: str(e)' + '\n'))

        # close the browser
        browser.close()
        pw.stop()


if __name__ == '__main__':
    scraper()
