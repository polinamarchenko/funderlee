from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import bs4
from project.startups.models import Startup
from project.investors.models import Investor, Market, InvestorsMarkets
import os

from project import db

market = Market(name="artificial intelligence")
category = market.name

browser = webdriver.Chrome()
browser.get('https://angel.co/login')
browser.find_element_by_css_selector('#user_email').send_keys(os.environ.get('ANGELLIST_EMAIL'))
browser.find_element_by_css_selector('#user_password').send_keys(os.environ.get('ANGELLIST_PASSWORD'))
browser.find_element_by_css_selector('.c-button.c-button--blue.s-vgPadLeft1_5.s-vgPadRight1_5').click()

browser.get('https://angel.co/people/investors')
sleep(1)
browser.find_element_by_css_selector('.search-box').click()
browser.find_element_by_css_selector('.input.inline-keyword-input.input-search').send_keys(category)
browser.find_element_by_css_selector('.input.inline-keyword-input.input-search').send_keys(Keys.RETURN)

WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 's-grid0')))

for i in range(0,7):
    sleep(2)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

soup_s = bs4.BeautifulSoup(browser.page_source, "html.parser")
show_s = soup_s.select("div.g-lockup.large > .text")

s_vals = [[val.select(".u-fontSize15 > a.u-colorGray3.u-uncoloredLink")[0].text, val.select(".u-fontSize15 > a.u-colorGray3.u-uncoloredLink")[0]['href']] for val in show_s]

locations = []
for val in show_s:
    el = val.select(".blurb.u-colorGray9.u-fontWeight300 > .s-vgTop0_5 > span.u-fontWeight400.u-colorGray6 > a")
    if len(el) > 0:
        locations.append(el[-1].text)
    else:
        locations.append('-')

investor_list = []

for (i,k) in enumerate(s_vals):
    found_investor = Investor.query.filter_by(name=s_vals[i][0]).first()
    if not found_investor:
        found_investor = Investor(name=s_vals[i][0], url=s_vals[i][1], country=locations[i])
        investor_list.append(found_investor)

    market.investors.append(found_investor)

    db.session.add(market)
    db.session.add(found_investor)

    db.session.add_all(investor_list)
    db.session.commit()



# Scraping startups
# browser = webdriver.Chrome()
# browser.get('https://angel.co/companies')
# sleep(1)
# browser.find_element_by_css_selector('.search-box').click()
# browser.find_element_by_css_selector('.keyword-input').send_keys(category)
# browser.find_element_by_css_selector('.keyword-input').send_keys(Keys.RETURN)
#
# WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))
#
# for i in range(0,7):
#     sleep(2)
#     browser.find_element_by_css_selector(".more").click()
#
# soup_s = bs4.BeautifulSoup(browser.page_source, "html.parser")
# show_s = soup_s.select("div.name")
# s_values = [[val.select(".startup-link")[0].text, val.select(".startup-link")[0]['href']] for val in show_s]
#
# startup_list = []
#
# for value in s_values:
# 	startup_list.append(Startup(name=value[0], url=value[1], market="biotech"))
#
# db.session.add_all(startup_list)
# db.session.commit()
