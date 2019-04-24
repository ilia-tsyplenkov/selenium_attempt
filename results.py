class Results:
    def __init__(self, driver, xpath):
        self.driver = driver
        self.xpath = xpath
        self.results = None

    def find_results(self):
        results = self.driver.find_elements_by_xpath(self.xpath)
        self.results = [x for x in results
                        if x.get_attribute('class') == 'ModelList__ModelBlockRow']

    def __getitem__(self, n):
        self.find_results()
        return self.results[n]

    def __len__(self):
        self.find_results()
        return len(self.results)
