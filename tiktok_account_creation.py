import requests
import random
import time
from captcha_bypass import solve_captcha
from proxy_setup import load_proxies

# Load proxies from the external file
proxy_file_path = 'proxies.txt'
proxies = load_proxies(proxy_file_path)

signup_url = "https://www.tiktok.com/signup"


def generate_random_username():
    return "user_" + str(random.randint(1000000, 9999999))


def generate_random_password():
    return "Pass_" + str(random.randint(1000000, 9999999))


def create_account(proxy):
    captcha_solution = solve_captcha("https://example.com/captcha_image.png")

    if captcha_solution:
        username = generate_random_username()
        password = generate_random_password()
        payload = {
            "username": username,
            "password": password,
            "captcha_solution": captcha_solution,
            # Add other required fields
        }
        response = requests.post(signup_url, data=payload, proxies={"http": proxy, "https": proxy})
        if response.status_code == 200:
            print(f"Account created successfully: {username}")
            return username, password
        else:
            print(f"Failed to create account: {response.status_code}")
            return None
    else:
        print("Captcha solving failed.")
        return None


def create_bulk_accounts(num_accounts):
    created_accounts = []
    for i in range(num_accounts):
        proxy = random.choice(proxies)
        account = create_account(proxy)
        if account:
            created_accounts.append(account)

        if i % 10 == 0 and i > 0:
            print(f"{i} accounts created. Taking a short break.")
            time.sleep(random.randint(30, 60))  # Pause between batches

    return created_accounts


def save_accounts(accounts, filename="created_accounts.txt"):
    with open(filename, "w") as f:
        for username, password in accounts:
            f.write(f"{username},{password}\n")
