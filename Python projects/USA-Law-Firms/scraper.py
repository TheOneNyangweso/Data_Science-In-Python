from playwright.sync_api import sync_playwright
from parsel import Selector
import pandas as pd
import csv
import time


def get_URLs():
    path_to_csv = '/home/nyangweso/Desktop/Ds_1/Data_Science-In-Python/Python projects/law_firm_links.csv'
    df = pd.read_csv(path_to_csv)
    link_list = [str(link) for link in df['links']]
    return link_list


def get_data():
    with sync_playwright() as pw:
        # Creating an empty DataFrame with the desired column names
        # columns = ['Name', 'Address', 'Location',
        #            'No_of_Partners', 'Phone', 'Website_URL']
        # data = pd.DataFrame(columns=columns)

        count = 655
        URLs = get_URLs()
        while count < 6786:
            try:
                print(f"starting iteration {count + 1}...")

                # Open a new browser for every 50 URLs
                if count % 50 == 0:
                    browser = pw.firefox.launch(headless=False)
                    page = browser.new_page()

                page.goto(URLs[count], timeout=120000,
                          wait_until='domcontentloaded')

                time.sleep(5)
                # get html
                html = page.content()
                # parse the HTML using parsel
                selector = Selector(text=html)
                

                name_of_law_firm = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/h1/text()').get()
                address = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/p[1]/text()').get()
                location = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/p[2]/text()').get()
                no_of_partners = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[2]/p/text()').get()
                phone = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[2]/div/div[3]/a/text()').get()
                website_url = selector.xpath(
                    '/html/body/main/div[3]/div[3]/div[1]/div[1]/div[3]/div/a/@href').get()

                row = [name_of_law_firm, address, location,
                       no_of_partners, phone, website_url]

                # Write directly to the CSV file
                with open('law_firm_data.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)

                count += 1
                # Close the browser and sleep for a minute after every 50 URLs
                if count % 50 == 0:
                    browser.close()
                    print("Sleeping for half a minute...")
                    time.sleep(30)

            except:
                with open("error_log.txt", 'a') as f:
                    f.write(str(f'iteration {count} failed\n'))
                count += 1
                continue

        # close the browser
        browser.close()
        pw.stop()
        return f"Scraped {count+1} pages."


if __name__ == '__main__':
    get_data()
