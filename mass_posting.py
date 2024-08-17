import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def load_proxies(file_path):
    """
    Load proxies from a file.

    :param file_path: Path to the file containing proxies.
    :return: A list of proxies.
    """
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines() if line.strip()]
    return proxies

def load_accounts(file_path):
    """
    Load TikTok accounts from a file.

    :param file_path: Path to the file containing account credentials.
    :return: A list of tuples containing (username, password).
    """
    accounts = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                accounts.append((parts[0], parts[1]))
    return accounts

def setup_driver(proxy=None):
    """
    Set up the Selenium WebDriver with optional proxy settings.

    :param proxy: A proxy string in the format 'http://user:pass@host:port'
    :return: An instance of a Selenium WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for faster execution
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_tiktok(driver, username, password):
    """
    Log into a TikTok account using the provided credentials.

    :param driver: A Selenium WebDriver instance.
    :param username: The TikTok username.
    :param password: The TikTok password.
    :return: True if login is successful, False otherwise.
    """
    try:
        driver.get("https://www.tiktok.com/login")
        time.sleep(3)

        # Locate username and password fields and log in
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login to complete

        # Check if login was successful
        if "login" in driver.current_url.lower():
            print(f"Login failed for {username}")
            return False
        print(f"Login successful for {username}")
        return True
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False

def post_content(driver, content):
    """
    Post content on the TikTok account.

    :param driver: A Selenium WebDriver instance.
    :param content: The content to post (e.g., a video file path).
    """
    try:
        driver.get("https://www.tiktok.com/upload")
        time.sleep(5)

        # Upload video file
        upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload_input.send_keys(content)

        time.sleep(5)

        # Find and click the post button
        post_button = driver.find_element(By.XPATH, "//button[contains(text(),'Post')]")
        ActionChains(driver).move_to_element(post_button).click(post_button).perform()

        print("Content posted successfully")
    except Exception as e:
        print(f"An error occurred while posting content: {e}")

def mass_post(accounts_file_path, content, proxies_file_path):
    """
    Mass post content on multiple TikTok accounts using proxies from a file.

    :param accounts_file_path: Path to the file containing account credentials.
    :param content: The content to post (e.g., a video file path).
    :param proxies_file_path: Path to the file containing proxies.
    """
    accounts = load_accounts(accounts_file_path)
    proxies = load_proxies(proxies_file_path)

    if len(accounts) > len(proxies):
        raise ValueError("The number of proxies must be at least equal to the number of accounts.")

    random.shuffle(proxies)  # Shuffle proxies for random assignment

    for i, account in enumerate(accounts):
        username, password = account
        proxy = proxies[i % len(proxies)]  # Rotate through proxies if fewer than accounts
        driver = setup_driver(proxy)

        if login_to_tiktok(driver, username, password):
            post_content(driver, content)
        driver.quit()

        # Pause between accounts to avoid detection
        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    # Example usage
    accounts_file_path = 'created_accounts.txt'  # Path to the accounts file
    content_to_post = "path/to/your/video.mp4"
    proxies_file_path = 'valid_proxies.txt'  # Path to the proxies file

    mass_post(accounts_file_path, content_to_post, proxies_file_path)
