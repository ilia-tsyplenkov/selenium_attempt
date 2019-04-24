import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def driver(request):
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")

    # this is like a teardonw in unittests
    def fin():
        driver.close()

    request.addfinalizer(fin)
    return driver
