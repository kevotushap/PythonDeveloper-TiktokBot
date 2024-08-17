from tiktok_account_creation import create_bulk_accounts, save_accounts
from account_warming import warm_up_accounts
from mass_posting import mass_post_to_accounts

def main():
    # Step 1: Create TikTok accounts
    print("Creating TikTok accounts...")
    created_accounts = create_bulk_accounts(100)  # Specify the number of accounts to create
    save_accounts(created_accounts)
    print("Account creation completed.")

    # Step 2: Warm up the accounts
    print("Warming up accounts...")
    warm_up_accounts(created_accounts)
    print("Account warming completed.")

    # Step 3: Mass post to accounts
    post_content = "This is a mass post to all accounts"
    print("Mass posting to accounts...")
    mass_post_to_accounts(created_accounts, post_content)
    print("Mass posting completed.")

if __name__ == "__main__":
    main()
