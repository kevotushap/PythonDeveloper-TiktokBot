from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from proxy_setup import load_proxies

# Load proxies from the external file
proxy_file_path = 'proxies.txt'
proxies = load_proxies(proxy_file_path)

driver_path = "/path/to/chromedriver"


def warm_up_account(username, password, proxy=None):
    options = webdriver.ChromeOptions()

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get("https://www.tiktok.com/login")

    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login

    for _ in range(5):
        driver.get("https://www.tiktok.com")
        time.sleep(10)  # Watch video for a while

    driver.quit()


def warm_up_accounts(accounts):
    for account in accounts:
        proxy = random.choice(proxies)  # Randomly select a proxy for each account
        warm_up_account(account[0], account[1], proxy)
