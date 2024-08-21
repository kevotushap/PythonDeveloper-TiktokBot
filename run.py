from tiktok_account_creation import create_bulk_accounts, save_accounts

def main():
    # Step 1: Create TikTok accounts
    print("Creating TikTok accounts...")
    created_accounts = create_bulk_accounts(100)  # Specify the number of accounts to create
    save_accounts(created_accounts)
    print("Account creation completed.")

if __name__ == "__main__":
    main()
