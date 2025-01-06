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

colorama.init(autoreset=True)

load_dotenv()

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def format_channel_username(channel_input):

    if channel_input.startswith('http://') or channel_input.startswith('https://'):
        channel_input = channel_input.split('//')[-1]
    if channel_input.startswith('t.me/'):
        channel_input = channel_input.split('t.me/')[-1]
    if channel_input.startswith('@'):
        channel_input = channel_input.lstrip('@')
    return channel_input.strip()

async def join_channel(client, channel_username):

async def process_message(client, message, text_file, media_dir, stats, semaphore):

async def scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None):

async def main():
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id:
        api_id = input("Enter your Telegram API ID: ")
    if not api_hash:
        api_hash = input("Enter your Telegram API Hash: ")

    try:
        api_id = int(api_id)
    except ValueError:
        print(Fore.RED + "Invalid API ID. It must be an integer.")
        return

    print(Fore.BLUE + "")
    channel_input = input("Enter the Telegram channel link or username (e.g., t.me/your_channel or your_channel): ")
    text_dir = input("Enter the directory to save text messages (e.g., texts): ")
    media_dir = input("Enter the directory to save media files (e.g., media): ")

    channel_username = format_channel_username(channel_input)

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)

    session_dir = os.path.join(application_path, 'session')
    os.makedirs(session_dir, exist_ok=True)

    session_path = os.path.join(session_dir, 'telegram_scraper')
    client = TelegramClient(session_path, api_id, api_hash)

    await client.start()

    await join_channel(client, channel_username)

    print(Fore.CYAN + "Scraping messages and media...")
    stats = await scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None)

    await client.disconnect()  # Disconnect the client when done


if __name__ == '__main__':
    asyncio.run(main())
