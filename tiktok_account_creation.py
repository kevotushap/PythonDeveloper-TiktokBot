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
    """Generate a random username for TikTok account creation."""
    return f"user_{random.randint(1000000, 9999999)}"


def generate_random_password():
    """Generate a random password for TikTok account creation."""
    return f"Pass_{random.randint(1000000, 9999999)}"


def create_account(proxy):
    """Create a single TikTok account using the provided proxy."""
    try:
        captcha_solution = solve_captcha("https://example.com/captcha_image.png")

        if not captcha_solution:
            print("Captcha solving failed.")
            return None

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
            print(f"Failed to create account: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error during account creation: {e}")
        return None


def create_bulk_accounts(num_accounts):
    """Create multiple TikTok accounts using a pool of proxies."""
    created_accounts = []
    for i in range(num_accounts):
        proxy = random.choice(proxies)
        account = create_account(proxy)
        if account:
            created_accounts.append(account)

        if i > 0 and i % 10 == 0:
            print(f"{i} accounts created. Taking a short break.")
            time.sleep(random.uniform(30, 60))  # Pause between batches

    return created_accounts


def save_accounts(accounts, filename="created_accounts.txt"):
    """Save the created accounts to a file."""
    try:
        with open(filename, "w") as f:
            for username, password in accounts:
                f.write(f"{username},{password}\n")
        print(f"Accounts saved to {filename}")
    except IOError as e:
        print(f"Failed to save accounts to {filename}: {e}")


if __name__ == "__main__":
    print("Starting bulk account creation...")
    accounts = create_bulk_accounts(100)  # Specify the number of accounts to create
    if accounts:
        save_accounts(accounts)
        print("Account creation completed.")
    else:
        print("No accounts were created.")
