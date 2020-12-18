#-*- coding:utf8 -*-
import os
import sys
import time
import logging
from selenium import webdriver

INLAND_URL = "https://www.rt-thread.org/account/user/index.html?response_type=code&authorized=yes&scope=basic&state=1588816557615&client_id=30792375&redirect_uri=https://club.rt-thread.org/index/user/login.html"
# FOREIGN_URL = "https://www.rt-thread.io/account/user/index.html?response_type=code&authorized=yes&scope=basic&state=1588816557615&client_id=26982367&redirect_uri=https://club.rt-thread.io/index/user/login.html"

# URL_LIST = [FOREIGN_URL, INLAND_URL]
URL_LIST = [INLAND_URL]

def login_in_club(user_name, pass_word):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=option, executable_path=r'/usr/bin/chromedriver')
    driver.maximize_window()

    # login in
    for club_url in URL_LIST:
        print("URL : {0}".format(club_url))
        driver.get(club_url)
        element = driver.find_element_by_id("username")
        element.send_keys(user_name)    
        element = driver.find_element_by_id('password')
        element.send_keys(pass_word)
        driver.find_element_by_id('login').click()
        time.sleep(10)

        if driver.current_url == "https://club.rt-thread.org/":
            try:
                element = driver.find_element_by_link_text(u"立即签到")
            except Exception as e:
                logging.error("Error message : {0}".format(e))
            else:
                element.click()
                logging.info("sign in success!")
        elif driver.current_url == "https://club.rt-thread.io/":
            try:  
                element = driver.find_element_by_link_text(u"Check in Now")
            except Exception as e:
                logging.error("Error message : {0}".format(e))
            else:
                element.click()
                logging.info("sign in success!")
        else:
            logging.error("username or password error, please check it, login in failed! {0}".format(driver.current_url));
            continue

        time.sleep(1)

        day_num = None
        # check sign in days
        try:
            element = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/a[1]")
        except Exception as e:
            logging.error("Error message : {0}".format(e))
        else:
            day_num = element.text
            if club_url.find("https://club.rt-thread.org/") != -1:
                logging.info("国内论坛: {0}".format(day_num))
            elif club_url.find("https://club.rt-thread.io/") != -1:
                logging.info("国外论坛: {0}".format(day_num))
            else:
                logging.error("username or password error, please check it, login in failed! {0}".format(driver.current_url));
                continue
    
    return 0;
