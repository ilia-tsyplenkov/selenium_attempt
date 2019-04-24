#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TODO: add module docs."""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException

COMPYTERS_MENU_ITEM = "Компьютеры"
LAPTOP_SUBMENU_ITEM = "Ноутбуки"

MIN_PRICE_ID = "minnum_45"
MAX_PRICE_ID = "maxnum_45"
min_price = "700"
max_price = "1500"
MANUFACTURE_EXPAND_XPATH = "//div[@id='Attr_prof_1000']/div[@class='ModelFilter__CharLine']/div[@class='ModelFilter__OpenHideAttr Page__DarkBgWapper']/span[@class='ModelFilter__OpenHideAttrTxt Page__DarkDotLink']"
MANUFACTURE_FILTER_XPATH = "//div[@id='Attr_prof_1000']/div[@class='ModelFilter__CharLine']/div[@class='ModelFilter__CheckboxLine ModelFilter__SlideAttrWapper ModelFilter__SlideAttrWapperOpen']/div[@class='ModelFilter__SlideLineInner']"

MANUFACTURE_EXPAND_CSS_SELECTOR = ".ModelFilter__OpenHideAttrTxt.Page__DarkDotLink"
DISPLAY_SIZE_LIST_ID = "Attr_prof_5828"
DISPLAY_SIZE_EXPAND_XPATH = "//div[@id='Attr_prof_5828']/div[@class='ModelFilter__CharLine']/div[@class='ModelFilter__OpenHideAttr Page__DarkBgWapper']/span[@class='ModelFilter__OpenHideAttrTxt Page__DarkDotLink']"

LENOVO_ID = 'prof_1000_8991'
CHECKBOX_XPATH_PATTERN = "label[@for='{0}']"
LENOVO_CHECKBOX_XPATH = "label[@for='{0}']".format(LENOVO_ID)
DELL_ID = 'prof_1000_2023'
DELL_CHECKBOX_XPATH = "//input[@id='prof_1000_2023']/label[1]"
HP_ID = 'prof_1000_1612'
HP_CHECKBOX_XPATH = "//input[@id='prof_1000_1612']/label[1]"
SHOW_RES_BUTTON = "ModelFilter__TxtBtnFormBlock"

SORTER_XPATH = "//div[@class='PanelSetUp__SelectionBlock']"

driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.implicitly_wait(3)

# driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))

try:
    driver.maximize_window()
    driver.get("https://shop.by/")
    actions = ActionChains(driver)
    computers = driver.find_element_by_link_text(COMPYTERS_MENU_ITEM)
    actions.move_to_element(computers).perform()
    laptops = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, LAPTOP_SUBMENU_ITEM)))
    laptops.click()

    start_price = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, MIN_PRICE_ID)))
    start_price.clear()
    start_price.send_keys(min_price)
    end_price = driver.find_element_by_id(MAX_PRICE_ID)
    end_price.clear()
    end_price.send_keys(max_price)
    end_price.submit()
    expand_manufacture_list = driver.find_element_by_xpath(MANUFACTURE_EXPAND_XPATH)
    actions = ActionChains(driver)
    actions.move_to_element(expand_manufacture_list).click().perform()
    actions.reset_actions()


    for link_text in ("Lenovo", "HP", "Dell"):
        elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        chk_box = driver.find_element_by_id("prof_1000_8991")
        driver.execute_script("window.scrollTo(0, %s)" % (int(elem.location['y']/2)))
        actions.move_to_element(elem).click().perform()
        actions.reset_actions()

    time.sleep(3)

    expand_display_size_list = driver.find_element_by_xpath(DISPLAY_SIZE_EXPAND_XPATH)
    driver.execute_script("window.scrollTo(0, %s)" % (int(expand_display_size_list.location['y']) - int(driver.get_window_size()['height'] / 2)))
    actions.move_to_element(expand_display_size_list).click().perform()
    actions.reset_actions()
    time.sleep(0.5)
    for link_text in ("12", "12.1", "12.5", "13", "13.1", "13.3", "13.4"):
        elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        driver.execute_script("window.scrollTo(0, %s)" % (int(elem.location['y'] - driver.get_window_size()['height']/2)))
        if elem.is_enabled():
            actions.move_to_element(elem).click().perform()
            actions.reset_actions()
    time.sleep(3)

    # print(driver.current_url)
    apply_button = driver.find_element_by_class_name("ModelFilter__TxtBtnFormBlock")
    apply_button.click()

    elem = driver.find_element_by_class_name("PageTip__WapperPanel")
    elem1 = elem.find_element_by_xpath("./div[1]/div[1]/div[2]/div[1]/span[1]")
    elem1.click()
    time.sleep(3)

    from_cheap = elem1.find_element_by_xpath("./span[2]/ul[1]/li[2]")
    from_cheap.click()

    result_page = driver.find_element_by_css_selector(".PageTip__DataList.Page__DataList")
    results = result_page.find_elements_by_xpath("./div[@class='ModelList']/div")
    results_on_page = 0
    print("items in results list: %s" % len(results))
    for item in results:
        class_name = item.get_attribute('class')
        if class_name == "ModelList__ModelBlockRow":
            results_on_page += 1
    print("%s results on the page" % results_on_page)

    first_elem = results[0]
    first_link = first_elem.find_element_by_xpath("./div[2]/div[1]/div[3]/div[1]").find_elements_by_tag_name('a')
    flink = first_link[0].get_attribute('href')

    elem = driver.find_element_by_class_name("PageTip__WapperPanel")
    elem1 = elem.find_element_by_xpath("./div[1]/div[1]/div[2]/div[1]/span[1]")
    elem1.click()
    from_expensive = elem1.find_element_by_xpath("./span[2]/ul[1]/li[3]")
    from_expensive.click()
    time.sleep(3)

    page_control = driver.find_element_by_xpath("//div[@itemtype='https://schema.org/ItemList']/div[2]/div[1]/div[1]")
    pages = page_control.find_elements_by_tag_name('a')
    pages[-2].click()
    time.sleep(3)

    result_page = driver.find_element_by_css_selector(".PageTip__DataList.Page__DataList")
    results = result_page.find_elements_by_xpath("./div[@class='ModelList']/div")
    last_elem = results[-1]
    last_link = last_elem.find_element_by_xpath("./div[2]/div[1]/div[3]/div[1]").find_elements_by_tag_name('a')
    llink = last_link[0].get_attribute("href")
    print(flink)
    print(llink)
    print(flink == llink)
finally:
    driver.close()
