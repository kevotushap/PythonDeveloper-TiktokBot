from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
from proxy_setup import load_proxies


def setup_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(service=Service('path/to/chromedriver'), options=chrome_options)
    return driver


def login_to_tiktok(driver, username, password):
    try:
        driver.get("https://www.tiktok.com/login")
        time.sleep(3)

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login to complete

        # Check if login was successful
        if "login" in driver.current_url.lower():
            raise Exception(f"Login failed for account {username}")

    except Exception as e:
        print(f"Error during login for account {username}: {e}")
        raise  # Re-raise exception for handling in the calling function


def warm_up_account(username, password, proxy=None):
    driver = setup_driver(proxy)
    try:
        login_to_tiktok(driver, username, password)

        # Simulate watching a few videos
        for _ in range(5):
            driver.get("https://www.tiktok.com")
            time.sleep(random.uniform(8, 15))  # Watch each video for a random time

        print(f"Account {username} warmed up successfully using proxy {proxy}")
    except Exception as e:
        print(f"Error warming up account {username}: {e}")
    finally:
        driver.quit()


def load_accounts(file_path='created_accounts.txt'):
    accounts = []
    with open(file_path, 'r') as f:
        for line in f:
            username, password = line.strip().split(',')
            accounts.append((username, password))
    return accounts


def warm_up_accounts():
    proxies = load_proxies('valid_proxies.txt')  # Load proxies from file
    accounts = load_accounts('created_accounts.txt')  # Load accounts from file

    proxy_usage = {}  # Track the usage of each proxy

    for account in accounts:
        # Dynamically choose a proxy that hasn't been used recently
        proxy = None
        if proxies:
            unused_proxies = [p for p in proxies if proxy_usage.get(p, 0) < 5]
            proxy = random.choice(unused_proxies if unused_proxies else proxies)
            proxy_usage[proxy] = proxy_usage.get(proxy, 0) + 1

        warm_up_account(account[0], account[1], proxy)
        time.sleep(random.uniform(30, 60))  # Random delay between warming up accounts

        # Reset proxy usage if all proxies have been used 5 times
        if all(count >= 5 for count in proxy_usage.values()):
            proxy_usage.clear()


# Example usage:
if __name__ == "__main__":
    warm_up_accounts()
