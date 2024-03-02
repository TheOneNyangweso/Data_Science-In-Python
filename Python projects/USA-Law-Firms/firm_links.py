from playwright.sync_api import sync_playwright
from parsel import Selector
import time
import pandas as pd


def get_firm_links():
    # count keeps track of successful iterations
    count = 193
    global links
    links = []
    try:
        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=False)
            page = browser.new_page()

            page.goto("https://law.usnews.com/law-firms/search?page=340",
                      timeout=120000, wait_until='domcontentloaded')

            var = 'button.page-numbers__Button-sc-138ov1k-4:nth-child(3)'

            # while count < 341:
                # get html
            html = page.content()
            # parse the HTML using parsel
            selector = Selector(text=html)
            for a in range(1, 7):
                href = [
                    selector.xpath(
                        f'/html/body/main/div[3]/div/div[4]/div[2]/div[1]/ol/li/div[1]/div[2]/div[{a}]/div[1]/div/a/text()').get(),
                    selector.xpath(
                        f'/html/body/main/div[3]/div/div[4]/div[2]/div[1]/ol/li/div[1]/div[2]/div[{a}]/div[4]/div/text()').get()
                ]
                print(href)
                links.append(href)

                time.sleep(5)
                # click "next page" button
                # page.click(selector=var)
                # if successful update counter
                # count += 1

            time.sleep(10)
            # screenshot is useful to know where the program crashed just in case
            page.screenshot(path='example.png')
            time.sleep(10)
            # close the browser
            browser.close()
            pw.stop()

            print(f'{count} loops successful')
    except:
        print(f'loop {count + 1} failed, rudi uteseke...')


if __name__ == '__main__':
    get_firm_links()
    df = pd.DataFrame(links, columns=['name', 'no_of_lawyers'])
    df.to_csv('law_firm_name_no_of_lawyers_3.csv', index=False)
