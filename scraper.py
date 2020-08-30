import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def configure_driver():
    """Configure headless firefox driver."""
    
    firefox_options = FirefoxOptions()
    
    # make the browser headless
    firefox_options.add_argument('--headless')

    # instantiate the webdriver
    driver = webdriver.Firefox(options = firefox_options)

    return driver


def main():
    driver = configure_driver()

    # this url is for the quikvol-tool page
    quikvol_url = 'https://www.cmegroup.com/tools-information/quikstrike/pricing-volatility-strategy-tools/quikvol-tool.html'
    # this url is for the EUU front month iframe
    EUU_iframe_url = 'https://cmegroup-tools.quikstrike.net//User/QuikStrikeView.aspx?pid=350&pf=61&viewitemid=AboutCMEHistory&insid=39113745'

    # not sure why I have to do it one after the other
    driver.get(quikvol_url)
    driver.get(EUU_iframe_url)

    try:
        # wait for container div to load
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'container'))
        )
    except TimeoutException as e:
        print('Timed out waiting for page to load.')

    data_points = iframe.find_elements(By.TAG_NAME, 'area')  # grab all area tags from the image map

    # print out data points from the 28th
    for point in data_points:
        fields = point.get_attribute('fields')
        if re.match(r'^date\|28', fields):
            print(fields)
    
    driver.quit()


if __name__ == '__main__':
    main()