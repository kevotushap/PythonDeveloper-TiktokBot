import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from proxy_setup import load_proxies

# Load proxies from the external file
proxy_file_path = 'proxies.txt'
proxies = load_proxies(proxy_file_path)

def initialize_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Configure proxy if provided
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    service = Service("/path/to/chromedriver")  # Update with path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_account(driver, username, password):
    login_url = "https://www.tiktok.com/login"
    driver.get(login_url)

    time.sleep(5)  # Wait for the page to load

    # Locate and fill in the login form (update selectors as needed)
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, '//button[text()="Login"]')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    time.sleep(10)  # Wait for login to complete

def warm_up_account(driver):
    # Example activities to warm up an account
    for _ in range(5):
        # Visit different pages
        driver.get("https://www.tiktok.com/trending")
        time.sleep(random.randint(5, 15))  # Random delay

        # Interact with content (like, follow, etc.)
        # Example of scrolling
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(5, 15))

        # Add more interactions as needed (like, comment, follow, etc.)

def main():
    accounts = [
        {"username": f"user{i}", "password": f"pass{i}"} for i in range(100)
    ]

    for i, account in enumerate(accounts):
        proxy = random.choice(proxies)  # Select a random proxy
        driver = initialize_driver(proxy=proxy)
        try:
            login_account(driver, account["username"], account["password"])
            warm_up_account(driver)
        except Exception as e:
            print(f"An error occurred with account {account['username']}: {e}")
        finally:
            driver.quit()

        # Optional: Take a break every 10 accounts to avoid detection
        if (i + 1) % 10 == 0:
            print(f"{i + 1} accounts processed. Taking a short break.")
            time.sleep(random.randint(30, 60))  # Pause between batches

if __name__ == "__main__":
    main()
