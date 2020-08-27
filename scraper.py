from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# https://www.cmegroup.com/tools-information/quikstrike/pricing-volatility-strategy-tools/quikvol-tool.html

def configure_driver():
    """Configure headless firefox driver."""
    
    firefox_options = FirefoxOptions()
    
    # make the browser headless
    firefox_options.add_argument("--headless")

    # instantiate the Webdriver
    driver = webdriver.Firefox(options = firefox_options)

    return driver

configure_driver()