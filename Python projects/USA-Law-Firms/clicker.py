from playwright.sync_api import sync_playwright
import time

# playwright = sync_playwright().start()

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless = False)
    page = browser.new_page()
    page.goto("https://law.usnews.com/law-firms/search")
    selector = 'button.page-numbers__Button-sc-138ov1k-4:nth-child(3)'
    # page.wait_for_timeout(timeout= 60000)
    
    for a in range(0,20):
        time.sleep(5)
        page.click(selector=selector)
    
    time.sleep(10)
    page.screenshot(path = 'example.png')
    time.sleep(10)
    # close the browser
    browser.close()
    pw.stop()
    print('20 loops successful')


# /html/body/main/div[3]/div/div[4]/div[2]/div[1]/nav/div[1]/button[2]
# button.page-numbers__Button-sc-138ov1k-4:nth-child(3)


