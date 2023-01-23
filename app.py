import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from config import load_config
from bot import send_message
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import time


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def find_day_in_week(session_date):
    date = datetime.strptime(session_date, '%d %b %Y')
    return date.strftime('%a')


def app(config):
    options = webdriver.ChromeOptions()
    options.set_headless()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(
        "C://Program Files (x86)/chromedriver.exe", options=options)

    username = config["bbdc"]["username"]
    password = config["bbdc"]["password"]
    bot_token = config["telegram"]["token"]
    chat_id = config["telegram"]["chat_id"]
    month_list = config["month_list"]

    browser.get("https://booking.bbdc.sg/#/login")
    idLogin = browser.find_element_by_id('input-8')
    idLogin.send_keys(username)
    idLogin = browser.find_element_by_id('input-15')
    idLogin.send_keys(password)
    loginButton = browser.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[1]/div/div/form/div/div[5]/button')
    loginButton.click()

    browser.implicitly_wait(10)
    browser.switch_to.default_content()
    bookingButton = browser.find_element_by_css_selector(
        '#app > div.v-application--wrap > div > nav > div.v-navigation-drawer__content > div.v-list.v-list.v-sheet.theme--light > div:nth-child(2)')
    bookingButton.click()

    practicalButton = browser.find_element_by_css_selector(
        '#app > div.v-application--wrap > div > main > div > div > div.flex.nav-web-view.d-none.d-md-flex > div > div.web-view.d-none.d-md-block > div > div > div.v-tabs.web-tabs.theme--light > div > div.v-slide-group__wrapper > div > div:nth-child(2)')
    practicalButton.click()

    browser.implicitly_wait(10)
    bookslotButton = browser.find_element_by_css_selector(
        '#app > div.v-application--wrap > div > main > div > div > div.flex.nav-web-view.d-none.d-md-flex > div > div.web-view.d-none.d-md-block > div > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div.v-window-item.v-window-item--active > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div > button')
    bookslotButton.click()

    browser.switch_to.default_content()
    nofixedInstructor = browser.find_element_by_css_selector(
        '#app > div.v-dialog__content.v-dialog__content--active > div > div > div.InstrutorTypeList > div > div > div.v-input__slot > div > div:nth-child(1)')
    nofixedInstructor.click()

    nextButton = browser.find_element_by_css_selector(
        '#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions > button')
    nextButton.click()

    def find_avil_classes():
        days = browser.find_elements_by_class_name(
            'v-calendar-weekly__day')
        for day in days:
            time.sleep(0.2)
            day.click()

    def next_month():
        nextMonthButton = browser.find_element_by_css_selector(
            '#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.justify-end > button.v-btn.v-btn--text.theme--light.v-size--default.primary--text')
        nextMonthButton.click()

    def add_message(message):
        sessionLists = browser.find_elements_by_class_name('sessionList')
        for i in range(len(sessionLists)):
            if i < (len(sessionLists)+1) // 2:
                sessionCards = sessionLists[i].find_elements_by_class_name(
                    'sessionCard')
                for j in range(len(sessionCards)):
                    if j < (len(sessionCards)+1)//2:
                        text_eles = sessionCards[j].find_elements_by_css_selector(
                            'div > p')
                        message_list = []
                        for text_ele in text_eles:
                            message_list.append(
                                text_ele.get_attribute('innerHTML').strip())
                        day_in_week = find_day_in_week(message_list[0])
                        message += f"\nDate: {message_list[0]} ({day_in_week}); Time: {message_list[2]}; Price: {message_list[3]}"
        return message

    # move on
    months = browser.find_elements_by_css_selector(
        '#app > div.v-application--wrap > div > main > div > div > div.flex.nav-web-view.d-none.d-md-flex > div > div.web-view.d-none.d-md-block > div.row > div.col-left.col.col-4 > div.calendar > div.dateList.dateList-web.d-none.d-md-flex > button')
    if months:
        message = "Session(s) available:"
        for i in range(len(months)):
            span = months[i].find_element_by_class_name('v-btn__content')
            span_text = span.get_attribute('innerHTML').strip()
            if span_text not in month_list:
                break
            months[i].click()
            if i > 0:
                next_month()
            time.sleep(4)
            find_avil_classes()
            message = add_message(message)
        print(message)
        send_message(message, bot_token, chat_id)
    else:
        message = "No session is available:("
        print(message)
        send_message(message, bot_token, chat_id)

    browser.quit()
