import logging
import os
import mimetypes
import asyncio
from collections import defaultdict
from telethon import TelegramClient
from telethon.errors import RPCError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
import colorama
from colorama import Fore, Style
from dotenv import load_dotenv
import sys

# Initialize colorama
colorama.init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Configure logging to write to a file
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def format_channel_username(channel_input):
    # Remove protocol and extract username
    if channel_input.startswith('http://') or channel_input.startswith('https://'):
        channel_input = channel_input.split('//')[-1]
    if channel_input.startswith('t.me/'):
        channel_input = channel_input.split('t.me/')[-1]
    if channel_input.startswith('@'):
        channel_input = channel_input.lstrip('@')
    return channel_input.strip()

async def join_channel(client, channel_username):
    # ... (Same as before)

async def process_message(client, message, text_file, media_dir, stats, semaphore):
    # ... (Same as before)

async def scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None):
    # ... (Same as before)

async def main():
    # Get API credentials from environment variables or prompt user to enter them
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id:
        api_id = input("Enter your Telegram API ID: ")
    if not api_hash:
        api_hash = input("Enter your Telegram API Hash: ")

    # Convert api_id to integer if it's not already
    try:
        api_id = int(api_id)
    except ValueError:
        print(Fore.RED + "Invalid API ID. It must be an integer.")
        return

    # Prompt the user for inputs
    print(Fore.BLUE + "")
    channel_input = input("Enter the Telegram channel link or username (e.g., t.me/your_channel or your_channel): ")
    text_dir = input("Enter the directory to save text messages (e.g., texts): ")
    media_dir = input("Enter the directory to save media files (e.g., media): ")

    # Format the channel username correctly
    channel_username = format_channel_username(channel_input)

    # Handle paths for PyInstaller
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)

    # Ensure session directory exists
    session_dir = os.path.join(application_path, 'session')
    os.makedirs(session_dir, exist_ok=True)

    # Create the Telegram client with a custom session path
    session_path = os.path.join(session_dir, 'telegram_scraper')
    client = TelegramClient(session_path, api_id, api_hash)

    # Start the client with automatic authentication if needed
    await client.start()

    await join_channel(client, channel_username)

    # Scrape messages and media after joining
    print(Fore.CYAN + "Scraping messages and media...")
    stats = await scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None)

    await client.disconnect()  # Disconnect the client when done

    # Provide a summary to the user
    # ... (Same as before)

if __name__ == '__main__':
    asyncio.run(main())
