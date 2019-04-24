

class Paginator:
    def __init__(self, driver, xpath):
        self.driver = driver
        self.xpath = xpath
        self.pages = None

    def load(self):
        paginator = self.driver.find_element_by_xpath(self.xpath)
        self.pages = paginator.find_elements_by_tag_name('a')

    def move_to_the_last(self):
        self.load()
        if len(self.pages) > 2:
            last_page = self.pages[-2]
        else:
            last_page = self.pages[-1]
        last_page.click()
