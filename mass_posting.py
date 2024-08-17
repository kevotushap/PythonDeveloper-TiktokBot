from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from proxy_setup import load_proxies

# Load proxies from the external file
proxy_file_path = 'proxies.txt'
proxies = load_proxies(proxy_file_path)

driver_path = "/path/to/chromedriver"


def mass_post(accounts, post_content, proxy=None):
    options = webdriver.ChromeOptions()

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get("https://www.tiktok.com/login")

    for account in accounts:
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(account[0])
        password_field.send_keys(account[1])
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login

        post_field = driver.find_element_by_name("post")
        post_field.send_keys(post_content)
        post_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for post to upload
        driver.quit()


def mass_post_to_accounts(accounts, post_content):
    for account in accounts:
        proxy = random.choice(proxies)  # Randomly select a proxy for each account
        mass_post([account], post_content, proxy)
