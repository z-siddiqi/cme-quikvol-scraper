import re
import datetime as dt
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main():
    driver = configure_driver()

    # this url is for the quikvol-tool page
    quikvol_url = 'https://www.cmegroup.com/tools-information/quikstrike/pricing-volatility-strategy-tools/quikvol-tool.html'
    # this url is for the EUU iframe
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

    # use the last data point to figure out the days to expiry
    last_data_point = parse_data(data_points[-1])

    if last_data_point['dte'] < 9:
        # change the futures contract selected to the next expiration
        change_contract(iframe, 1)

        # grab previous weekdays area tags from the image map
        area_tags = iframe.find_elements(By.XPATH, f'//area[starts-with(@fields, "date|{prev_weekday}")]')
        data_points = [point.get_attribute('fields') for point in area_tags]  # the fields attribute has all of the required data

    for data_point in data_points:
        if 'future' not in data_point and 'ratio' not in data_point:
            print(parse_data(data_point))
    
    driver.quit()


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


def change_contract(frame, exp):
    """Changes the futures contract selected using the expirations dropdown."""

    # open up expirations dropdown
    exp_ddelem = frame.find_element(By.XPATH, '//*[@id="MainContent_ucViewControl_ActiveVol_tbATM_ucExpirationPicker_ucTrigger_lnkTrigger"]')
    exp_ddelem.click()

    # untick current expiration
    latest_exp = exp_ddelem.find_element(By.XPATH, '//*[@id="MainContent_ucViewControl_ActiveVol_tbATM_ucExpirationPicker_lvPopGroups2_lvExpirations_0_cbExpiration_0"]')
    latest_exp.click()

    try:
        # tick new expiration
        new_exp = exp_ddelem.find_element(By.XPATH, f'//*[@id="MainContent_ucViewControl_ActiveVol_tbATM_ucExpirationPicker_lvPopGroups2_lvExpirations_0_cbExpiration_{exp}"]')
        new_exp.click()
    except NoSuchElementException as e:
        print('Can\'t change to that expiration date, element does not exist!')

    # click ok button
    ok_button = exp_ddelem.find_element(By.XPATH, '//*[@id="MainContent_ucViewControl_ActiveVol_tbATM_ucExpirationPicker_btnOK"]')
    ok_button.click()

    # wait for page to load fully
    time.sleep(5)


def parse_data(data):
    """Parses scraped data and stores it in a dictionary."""

    # use regex to find the required data
    date_string = re.search(r'date\|[0-9]{2}/[0-9]{2}/[0-9]{4}', data)
    vol_string = re.search(r'vol\|[0-9]+\.[0-9]{1,2}$', data)
    days_to_exp_string = re.search(r'dte\|[0-9]{1,3}', data)

    # handle re.search returning NoneType
    if date_string:
        date_string = date_string.group(0)[5:]
        date = dt.datetime.strptime(date_string, '%d/%m/%Y').date()
    else:
        date = None

    if vol_string:
        vol_string = vol_string.group(0)[4:]
        vol = float(vol_string)
    else:
        vol = None
    
    if days_to_exp_string:
        days_to_exp_string = days_to_exp_string.group(0)[4:]
        days_to_exp = int(days_to_exp_string)
    else:
        days_to_exp = None

    vol_type = 'IV' if 'atmStrike' in data else 'HV'
    parsed_data = {'date': date, 'type': vol_type, 'vol': vol, 'dte': days_to_exp}

    return parsed_data


if __name__ == '__main__':
    main()