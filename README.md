Telegram Channel Scraper
This script allows you to scrape messages and media from a Telegram channel.

Table of Contents
Requirements
Setup
1. Obtain Telegram API Credentials
2. Set Up Environment Variables
Option A: Using a .env File (Recommended)
Option B: Entering API Credentials Manually
3. Running the Script
Step 1: Execute the Script
Step 2: Enter the Telegram Channel Link
Step 3: Specify Directories to Save Data
Step 4: Enter Your Telegram Phone Number
Step 5: Enter the Verification Code
Step 6: Scraping Begins
Step 7: Completion
Additional Information
Session File Management
Dependencies
API Credentials Security
Disclaimer
Requirements
Python 3.7 or higher
Telegram API credentials (API ID and API Hash)
Telegram account (with access to the target channel)
Setup
1. Obtain Telegram API Credentials
Go to my.telegram.org and log in with your Telegram account.
Enter your Telegram phone number.
Fill in the required details to get your API ID and API Hash.
2. Set Up Environment Variables
Option A: Using a .env File (Recommended)
Create a file named .env in the project directory.

Add your API credentials to the file:

INI

TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
Replace your_api_id and your_api_hash with your actual credentials.

Option B: Entering API Credentials Manually
If you don't want to use a .env file, you can run the script without it. The script will prompt you to input your API ID and API Hash when you execute it.

3. Running the Script
Step 1: Execute the Script
Run the script using Python:

BASH

python3 scrape.py
Step 2: Enter the Telegram Channel Link
The script will prompt you to enter the Telegram channel link or username:


Enter the Telegram channel link or username (e.g., t.me/your_channel or your_channel):
You can enter the channel link in various formats:
t.me/your_channel
https://t.me/your_channel
@your_channel
your_channel
Step 3: Specify Directories to Save Data
You'll be asked to specify the directories where the scraped data will be saved:


Enter the directory to save text messages (e.g., texts):
Enter the directory to save media files (e.g., media):
Directory to save text messages: The script will save the scraped text messages in this directory.
Directory to save media files: The script will download media files (photos, videos, documents, etc.) to this directory.
Step 4: Enter Your Telegram Phone Number
The script will prompt you to enter your Telegram phone number for authentication:


Please enter your phone (or bot token):
Enter your phone number associated with your Telegram account, including the country code (e.g., +1234567890).
Step 5: Enter the Verification Code
Telegram will send a verification code to your Telegram app (or via SMS, depending on your settings).

The script will prompt you to enter the code:


Please enter the code you received:
Enter the code exactly as it appears in your Telegram app.

Step 6: Scraping Begins
Once authenticated, the script will start scraping messages and media from the specified channel.

Progress messages will be displayed in the console.
The script will output the status of media downloads and any errors encountered.
Step 7: Completion
After scraping is complete, the script will display a summary:


Scraping Completed!
Total messages scraped: [number]
Messages saved to: [path to messages.txt]

Media files downloaded:
  Photos: [count]
  Videos: [count]
  Documents: [count]
  ...
Media files saved to: [path to media directory]
Note: If you have already authenticated (i.e., a session file exists), the script will not prompt you to enter your phone number and code again unless the session expires or is deleted.

Additional Information
Session File Management
The script creates a session file (telegram_scraper.session) in the session directory.
This session file keeps you authenticated between runs.
Do not share this file or commit it to version control repositories like GitHub.
If you delete the session file or it becomes invalid, you will need to re-authenticate by entering your phone number and the code sent by Telegram.
Dependencies
Ensure you have installed all required Python packages:

BASH

pip install -r requirements.txt
If you don't have a requirements.txt file, you can install the packages individually:

BASH

pip install telethon colorama python-dotenv
API Credentials Security
Keep your API ID and API Hash secure.
Do not share your credentials with others.
If using a .env file, make sure to include it in your .gitignore file to prevent it from being uploaded to public repositories.
Disclaimer
This script is intended for educational and personal use. Please adhere to Telegram's Terms of Service and respect the privacy and rights of others. The author is not responsible for any misuse of this script.
