import csv
import os
from parsel import Selector
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

writer = csv.writer(open('profile_linked.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name','Posistion','Company','Education','Location','URL'])

time_start = time()
# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome(os.getcwd() +"/chromebrowser/chromedriver")
driver.get("https://linkedin.com/")

username = driver.find_element_by_name("session_key")
username.send_keys('xxxxxx@xxxxx.com')
sleep(0.5)

password = driver.find_element_by_name('session_password')
password.send_keys('xxxxxxx')
sleep(0.5)

sign_in_btn = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_btn.click()
sleep(2)

driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in AND "python developer" AND "indonesia"')
search_query.send_keys(Keys.RETURN)
sleep(0.5)

urls = driver.find_elements_by_xpath('//*[@class = "r"]/a[@href]')
urls = [url.get_attribute('href') for url in urls]
sleep(0.5)

for url in urls:
    driver.get(url)
    sleep(2)

    sel = Selector(text=driver.page_source)
    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)
    position = sel.css('.t-18::text').get()

    # experience = sel.xpath('//*[@class = "pv-profile-section-pager ember-view"]')
    # company = experience.xpath('./li[@class = "pv-entity__position-group-pager pv-profile-section__list-item ember-view"]//p[@class = "pv-entity__secondary-title t-14 t-black t-normal"]/text()').extract_first()
    # company = ', '.join(company) if company else None
    company = sel.css('#experience-section p.pv-entity__secondary-title::text').getall()
    print(company)
    company = ', '.join(company) if company else None

    # education = experience.xpath('')
    url = driver.current_url
    time_end = time()
    print('\n')
    print('Name: {}'.format(name))
    print('Position: {}'.format(position.strip()))
    print('Company: {}'.format(company))
    print("time : {}".format(time_end - time_start))
    time_end = 0

driver.quit()