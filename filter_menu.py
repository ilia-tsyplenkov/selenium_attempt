from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import common


class BaseFilterMenu:
    def __init__(self, driver, expand_link_xpath):
        self.driver = driver
        self.expand_link_xpath = expand_link_xpath
        self.actions = ActionChains(self.driver)

    def place_to_center(self, elem):
        script = "window.scrollTo(0, {})".format(int(elem.location['y'] -
                                                     self.driver.get_window_size()['height'] / 2))
        self.driver.execute_script(script)

    def expand(self, centered=True):
        expand_link = self.driver.find_element_by_xpath(self.expand_link_xpath)
        if centered:
            self.place_to_center(expand_link)
        self.actions.move_to_element(expand_link).click().perform()
        self.actions.reset_actions()

    def click_on_items(self, list_items):

        for text in list_items:
            elem = WebDriverWait(self.driver, common.COMMON_TIMEOUT).until(
                EC.presence_of_element_located((By.LINK_TEXT, text)))
            # self.place_to_center(elem)
            self.actions.move_to_element(elem).click().perform()
            self.actions.reset_actions()
