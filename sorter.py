from selenium.webdriver.common.action_chains import ActionChains


class SortMenu:
    def __init__(self, driver, menu_xpath, items_xpaths):
        self.driver = driver
        self.xpath = menu_xpath
        self.items_xpaths = items_xpaths
        self.menu = None
        self.items = None
        self.actions = ActionChains(self.driver)

    def find_menu_elements(self):
        self.menu = self.driver.find_element_by_xpath(self.xpath)
        self.items = dict((x, self.menu.find_element_by_xpath(y))
                          for (x, y) in self.items_xpaths.items())

    def select(self, item_name):
        self.find_menu_elements()
        self.actions.move_to_element(self.menu).click().perform()
        self.actions.reset_actions()
        item = self.items[item_name]
        item.click()
