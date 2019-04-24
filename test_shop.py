#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TODO: add module docs."""

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from filter_menu import BaseFilterMenu
from sorter import SortMenu
from results import Results
from paginator import Paginator
from common import COMMON_TIMEOUT, get_catalog_item, set_price_range, result_item_link

COMPUTERS_MENU_ITEM = "Компьютеры"
LAPTOP_SUBMENU_ITEM = "Ноутбуки"

min_price = "700"
max_price = "1500"
MANUFACTURE_EXPAND_XPATH = "//div[@id='Attr_prof_1000']/div[@class='ModelFilter__CharLine']" \
                           "/div[@class='ModelFilter__OpenHideAttr Page__DarkBgWapper']/" \
                           "span[@class='ModelFilter__OpenHideAttrTxt Page__DarkDotLink']"

DISPLAY_SIZE_EXPAND_XPATH = "//div[@id='Attr_prof_5828']/div[@class='ModelFilter__CharLine']" \
                            "/div[@class='ModelFilter__OpenHideAttr Page__DarkBgWapper']" \
                            "/span[@class='ModelFilter__OpenHideAttrTxt Page__DarkDotLink']"

SHOW_RES_BUTTON = "ModelFilter__TxtBtnFormBlock"

SORTER_XPATH = "//div[@class='PageTip__WapperPanel']/div[1]/div[1]/div[2]/div[1]/span[1]"
SORTER_ITEMS = {"from_cheap": "./span[2]/ul[1]/li[2]",
                "from_expensive": "./span[2]/ul[1]/li[3]"}

RESULTS_XPATH = "//div[@itemtype='https://schema.org/ItemList']/div[1]/div[@class='ModelList']/div"
PAGINATOR_XPATH = "//div[@itemtype='https://schema.org/ItemList']/div[2]/div[1]/div[1]"

MANUFACTORY_LIST = ("Lenovo", "HP", "Dell")
DISPLAY_SIZE_LIST = ("12", "12.1", "12.5", "13", "13.1", "13.3", "13.4")

driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.implicitly_wait(3)


try:
    driver.maximize_window()
    driver.get("https://shop.by/")
    actions = ActionChains(driver)
    laptops = get_catalog_item(driver, COMPUTERS_MENU_ITEM, LAPTOP_SUBMENU_ITEM)
    actions.move_to_element(laptops).click().perform()
    actions.reset_actions()

    if "noutbuki" not in driver.current_url:
        raise Exception("Redirect to /%s page doesn't happened" % "noutbuki")

    set_price_range(driver, min_price, max_price)
    manufacture_filter = BaseFilterMenu(driver, MANUFACTURE_EXPAND_XPATH)
    manufacture_filter.expand()
    manufacture_filter.click_on_items(MANUFACTORY_LIST)

    time.sleep(COMMON_TIMEOUT)

    display_size_filter = BaseFilterMenu(driver, DISPLAY_SIZE_EXPAND_XPATH)
    display_size_filter.expand()
    display_size_filter.click_on_items(DISPLAY_SIZE_LIST)

    time.sleep(COMMON_TIMEOUT)

    filter_url = driver.current_url
    apply_button = driver.find_element_by_class_name(SHOW_RES_BUTTON)
    apply_button.click()

    if driver.current_url == filter_url:
        raise Exception("Redirect on result page is not happened.")

    sorter = SortMenu(driver, SORTER_XPATH, SORTER_ITEMS)
    sorter.select("from_cheap")

    results = Results(driver, RESULTS_XPATH)
    print("%s results on the page" % len(results))

    flink = result_item_link(results[0])

    sorter.select("from_expensive")
    time.sleep(3)

    paginator = Paginator(driver, PAGINATOR_XPATH)
    paginator.move_to_the_last()

    time.sleep(COMMON_TIMEOUT)

    llink = result_item_link(results[-1])
    print(flink)
    print(llink)
    print(flink == llink)
finally:
    driver.close()
