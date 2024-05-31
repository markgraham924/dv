# utils/auth.py
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from .env import set_env_variable, get_env_variable
import requests

def fetch_upc_data(store_number, upc):
    if not check_headers_validity():
        raise ValueError("Authorization or cookie header is missing or expired.")

    authorization_header = get_env_variable('AUTHORIZATION_HEADER')
    cookie_header = get_env_variable('COOKIE_HEADER')

    url = f"https://foods-sst.marksandspencer.app/api/sst/upcData?storeNumber={store_number}&GhostUPC={upc}&ParentUPC={upc}&usermode=ALL"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,es;q=0.8,la;q=0.7,fr;q=0.6",
        "authorization": authorization_header,
        "cookie": cookie_header,
        "dnt": "1",
        "referer": "https://foods-sst.marksandspencer.app/home/deliveries",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

def fetch_drn_list(store_code):
    if not check_headers_validity():
        raise ValueError("Authorization or cookie header is missing or expired.")

    authorization_header = get_env_variable('AUTHORIZATION_HEADER')
    cookie_header = get_env_variable('COOKIE_HEADER')

    url = f"https://foods-sst.marksandspencer.app/api/rapidCheck/drnList?storeCode={store_code}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,es;q=0.8,la;q=0.7,fr;q=0.6",
        "authorization": authorization_header,
        "cookie": cookie_header,
        "dnt": "1",
        "referer": "https://foods-sst.marksandspencer.app/home/deliveries",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

def fetch_pallet_summary(drn, store_code):
    if not check_headers_validity():
        raise ValueError("Authorization or cookie header is missing or expired.")

    authorization_header = get_env_variable('AUTHORIZATION_HEADER')
    cookie_header = get_env_variable('COOKIE_HEADER')

    url = f"https://foods-sst.marksandspencer.app/api/rapidCheck/palletSummary?drn={drn}&storeCode={store_code}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,es;q=0.8,la;q=0.7,fr;q=0.6",
        "authorization": authorization_header,
        "cookie": cookie_header,
        "dnt": "1",
        "referer": "https://foods-sst.marksandspencer.app/home/deliveries",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

def get_auth_and_cookie(username, password, store_number):
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = wire_webdriver.Chrome(options=chrome_options)

    url = 'https://foods-sst.marksandspencer.app/home'

    try:
        driver.get(url)
        time.sleep(5)

        driver.find_element(By.ID, 'i0116').send_keys(username)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        driver.find_element(By.ID, 'i0118').send_keys(password)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(3)

        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(5)

        driver.find_element(By.ID, 'inputStoreCode').send_keys(store_number)
        driver.find_element(By.CLASS_NAME, 'submit').click()
        time.sleep(3)

        cookie_header = None
        authorization_header = None

        for request in driver.requests:
            if request.response:
                if (f"https://foods-sst.marksandspencer.app/api/sst/summarygraph?storeNumber={store_number}" in request.url):
                    headers = request.headers
                    cookie_header = headers.get('cookie')
                    authorization_header = headers.get('authorization')
                    break

        if authorization_header and cookie_header:
            set_env_variable('AUTHORIZATION_HEADER', authorization_header)
            set_env_variable('COOKIE_HEADER', cookie_header)
            set_env_variable('TIMESTAMP', datetime.utcnow().isoformat())

        return authorization_header, cookie_header

    finally:
        driver.quit()

def check_headers_validity():
    timestamp = get_env_variable('TIMESTAMP')
    if not timestamp:
        return False

    timestamp = datetime.fromisoformat(timestamp)
    if datetime.utcnow() - timestamp < timedelta(hours=1):
        return True
    else:
        return False

def get_stored_headers():
    auth = get_env_variable('AUTHORIZATION_HEADER')
    cookie = get_env_variable('COOKIE_HEADER')
    return auth, cookie
