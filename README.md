PythonDeveloper-TiktokBot
PythonDeveloper-TiktokBot is a Python-based automation tool designed to create, warm up, and manage multiple TikTok accounts using proxies to avoid bans. The bot also includes functionality for bypassing CAPTCHA challenges and mass posting to all accounts.

Features
TikTok Account Creation: Create unlimited TikTok accounts using random credentials.
CAPTCHA Bypass: Integrate with sadcaptcha.com for solving CAPTCHA challenges automatically.
Proxy Support: Load proxies from an external file to prevent accounts from being banned.
Account Warming: Automate the process of warming up accounts by watching videos using Selenium.
Mass Posting: Post content to multiple TikTok accounts simultaneously.
Project Structure
graphql
Copy code
PythonDeveloper-TiktokBot/
│
├── captcha_bypass.py          # CAPTCHA solving module using sadcaptcha.com API
├── tiktok_account_creation.py # Handles TikTok account creation
├── account_warming.py         # Warms up TikTok accounts by watching videos
├── mass_posting.py            # Manages mass posting to all created accounts
├── proxy_setup.py             # Loads and tests proxies from an external file
├── run.py                     # Main script to run the bot
├── created_accounts.txt       # Stores the credentials of created accounts
├── proxies.txt                # Stores the list of proxies to be used
└── README.md                  # Project documentation
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/PythonDeveloper-TiktokBot.git
cd PythonDeveloper-TiktokBot
Install Dependencies:

Ensure you have Python 3.x installed, then run:

bash
Copy code
pip install -r requirements.txt
Setup Proxies:

Add your proxies to proxies.txt (one proxy per line):

perl
Copy code
http://username:password@proxy1.com:port
http://username:password@proxy2.com:port
...
Setup CAPTCHA Bypass:

Ensure you have an account with sadcaptcha.com and update the solve_captcha function in captcha_bypass.py with your API details.

Usage
Run the Bot:

The main entry point is run.py. You can execute it using:

bash
Copy code
python run.py
Creating Accounts:

The bot will create TikTok accounts using the proxies provided in proxies.txt and save the credentials in created_accounts.txt.

Warming Up Accounts:

After creating the accounts, the bot will automatically warm them up by watching videos on TikTok.

Mass Posting:

Once the accounts are warmed up, you can mass post content to all the created accounts.

Configuration
Proxies: Edit the proxies.txt file to add or remove proxies.
Account Credentials: The created account credentials are stored in created_accounts.txt.
CAPTCHA Bypass: Update the solve_captcha function in captcha_bypass.py with the correct API details.
Contributing
Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit a pull request.

License
This project is licensed under the MIT License.

Acknowledgements
Selenium for browser automation.
sadcaptcha.com for CAPTCHA solving API.
TikTok for the platform.
