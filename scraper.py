import re
import datetime as dt

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def configure_driver():
    """Configures a headless firefox driver."""
    
    firefox_options = FirefoxOptions()
    
    # make the browser headless
    firefox_options.add_argument('--headless')

    # instantiate the webdriver
    driver = webdriver.Firefox(options = firefox_options)

    return driver


def get_prev_weekday(some_date):
    """Calculates the date of the previous weekday."""

    some_date -= dt.timedelta(days=1)
    while some_date.weekday() > 4:
        some_date -= dt.timedelta(days=1)
    
    return some_date


def parse_data(data):
    """Parses scraped data and stores it in a dictionary."""

    # use regex to find the required data
    date_string = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', data).group(0)
    vol_string = re.search(r'[0-9]+\.[0-9]{1,2}$', data).group(0)

    date = dt.datetime.strptime(date_string, '%d/%m/%Y').date()
    vol_type = 'IV' if 'atmStrike' in data else 'HV'
    vol = float(vol_string)
    parsed_data = {'date': date, 'type': vol_type, 'vol': vol}

    return parsed_data


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

    todays_date = dt.datetime.today()
    prev_weekday = get_prev_weekday(todays_date).strftime('%d/%m/%Y')

    # grab previous weekdays area tags from the image map
    area_tags = iframe.find_elements(By.XPATH, f'//area[starts-with(@fields, "date|{prev_weekday}")]')
    data_points = [point.get_attribute('fields') for point in area_tags]  # the fields attribute has all of the required data

    for data_point in data_points:
        if 'future' not in data_point and 'ratio' not in data_point:
            print(parse_data(data_point))
    
    driver.quit()


if __name__ == '__main__':
    main()