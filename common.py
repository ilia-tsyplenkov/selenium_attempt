from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

COMMON_TIMEOUT = 5
SMALL_TIMEOUT = 0.5
MIN_PRICE_ID = "minnum_45"
MAX_PRICE_ID = "maxnum_45"


def get_catalog_item(driver, menu_item, submenu_item=None):
    general_item = driver.find_element_by_link_text(menu_item)
    if not submenu_item:
        return general_item
    actions = ActionChains(driver)
    actions.move_to_element(general_item).perform()
    return WebDriverWait(driver, COMMON_TIMEOUT).until(
        EC.presence_of_element_located((By.LINK_TEXT, submenu_item)))


def set_price_range(driver, min_price=None, max_price=None):
    start_price = WebDriverWait(driver, COMMON_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, MIN_PRICE_ID)))
    if min_price:
        start_price.clear()
        start_price.send_keys(min_price)
    end_price = driver.find_element_by_id(MAX_PRICE_ID)
    if max_price:
        end_price.clear()
        end_price.send_keys(max_price)
    end_price.submit()


def result_item_link(item):
    a_tag = item.find_element_by_xpath("./div[2]/div[1]/div[3]/div[1]").find_elements_by_tag_name('a')
    return a_tag[0].get_attribute("href")
