import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from proxy_setup import load_proxies

# Load proxies from the external file
proxy_file_path = 'proxies.txt'
proxies = load_proxies(proxy_file_path)

signup_url = "https://www.tiktok.com/signup"

def solve_captcha(captcha_image_url):
    api_url = "https://www.sadcaptcha.com/api/solve"
    data = {
        'image_url': captcha_image_url,
        'ref': 'angell'  # Replace with your actual referral code if applicable
    }
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        solution = response.json().get('solution')
        if solution:
            return solution
        else:
            raise Exception("CAPTCHA solution not found in the response.")
    else:
        raise Exception(f"Failed to solve CAPTCHA. Status Code: {response.status_code}")

def get_captcha_image_url(signup_url):
    # Configure WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
    service = Service("/path/to/chromedriver")  # Update with path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(signup_url)

        # Give the page some time to load
        time.sleep(5)

        # Locate the CAPTCHA image element (Update the selector based on TikTok's actual page structure)
        captcha_image_element = driver.find_element(By.CSS_SELECTOR, "img.captcha-image")
        captcha_image_url = captcha_image_element.get_attribute("src")
        return captcha_image_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

def generate_random_username():
    return "user_" + str(random.randint(1000000, 9999999))

def generate_random_password():
    return "Pass_" + str(random.randint(1000000, 9999999))

def create_account(proxy):
    try:
        captcha_image_url = get_captcha_image_url(signup_url)
        if not captcha_image_url:
            print("Failed to retrieve CAPTCHA image URL.")
            return None

        captcha_solution = solve_captcha(captcha_image_url)

        if captcha_solution:
            username = generate_random_username()
            password = generate_random_password()
            payload = {
                "username": username,
                "password": password,
                "captcha_solution": captcha_solution,
                # Add other required fields for the signup form
            }

            response = requests.post(signup_url, data=payload, proxies={"http": proxy, "https": proxy})

            if response.status_code == 200:
                print(f"Account created successfully: {username}")
                return username, password
            else:
                print(f"Failed to create account: HTTP {response.status_code} - {response.text}")
                return None
        else:
            print("Captcha solving failed.")
            return None
    except Exception as e:
        print(f"An error occurred during account creation: {e}")
        return None

def create_bulk_accounts(num_accounts):
    created_accounts = []
    for i in range(num_accounts):
        proxy = random.choice(proxies)
        account = create_account(proxy)
        if account:
            created_accounts.append(account)

        # Take a break every 10 accounts to avoid detection
        if i % 10 == 0 and i > 0:
            print(f"{i} accounts created. Taking a short break.")
            time.sleep(random.randint(30, 60))  # Pause between batches

    return created_accounts

def save_accounts(accounts, filename="created_accounts.txt"):
    with open(filename, "w") as f:
        for username, password in accounts:
            f.write(f"{username},{password}\n")

    print(f"Accounts saved to {filename}")

