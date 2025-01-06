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
    try:
        await client(JoinChannelRequest(channel_username))
        message = f"Successfully joined the channel @{channel_username}"
        print(Fore.GREEN + message)
        logger.info(message)
    except RPCError as e:
        error_message = f"Failed to join channel @{channel_username}: {e}"
        print(Fore.RED + f"Error: {error_message}")
        logger.error(error_message)

async def process_message(client, message, text_file, media_dir, stats, semaphore):
    try:
        async with semaphore:
            # Save text messages
            message_str = message.stringify()
            text_file.write(f"{message_str}\n\n")
            logger.info(f"Scraped message ID {message.id}")
            stats['messages'] += 1

            # Download all media types
            if message.media:
                file_name = None
                if message.file and message.file.name:
                    file_name = message.file.name
                else:
                    mime_type = message.file.mime_type if message.file else None
                    extension = mimetypes.guess_extension(mime_type) if mime_type else ''
                    file_name = f"media_{message.id}{extension}"

                if file_name:
                    file_name = os.path.basename(file_name)
                    file_path = os.path.join(media_dir, file_name)
                    result = await message.download_media(file=file_path)
                    if result:
                        media_type = message.file.mime_type.split('/')[0] if message.file and message.file.mime_type else 'unknown'
                        stats['media'][media_type] += 1
                        print(Fore.YELLOW + f"Downloaded {media_type}: {file_path}")
                        logger.info(f"Downloaded {media_type} ID {message.id} to {file_path}")
                    else:
                        print(Fore.RED + f"Failed to download media ID {message.id}")
                        logger.warning(f"Failed to download media ID {message.id}")
    except FloodWaitError as e:
        wait_time = e.seconds + 5  # Add buffer
        print(Fore.RED + f"Rate limit exceeded. Waiting for {wait_time} seconds...")
        logger.warning(f"FloodWaitError: Waiting for {wait_time} seconds")
        await asyncio.sleep(wait_time)
    except Exception as e:
        error_message = f"An error occurred while processing message ID {message.id}: {e}"
        print(Fore.RED + f"Error: {error_message}")
        logger.error(error_message)

async def scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None):
    stats = {
        'messages': 0,
        'media': defaultdict(int)  # Dictionary to count different media types
    }

    try:
        if not os.path.exists(text_dir):
            os.makedirs(text_dir)
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        text_file_path = os.path.join(text_dir, 'messages.txt')

        # Semaphore to limit concurrency
        semaphore = asyncio.Semaphore(10)  # Adjust the number as needed

        tasks = []

        with open(text_file_path, 'a', encoding='utf-8') as text_file:
            print(Fore.CYAN + f"Starting to scrape messages from @{channel_username}...")
            async for message in client.iter_messages(channel_username, limit=limit):
                # Collect tasks for concurrent execution
                task = asyncio.create_task(process_message(client, message, text_file, media_dir, stats, semaphore))
                tasks.append(task)

            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

            print(Fore.CYAN + f"Finished scraping messages from @{channel_username}.")
            return stats

    except RPCError as e:
        error_message = f"Failed to scrape messages from @{channel_username}: {e}"
        print(Fore.RED + f"Error: {error_message}")
        logger.error(error_message)
        return stats
    except Exception as e:
        error_message = f"An unexpected error occurred while scraping messages from @{channel_username}: {e}"
        print(Fore.RED + f"Error: {error_message}")
        logger.error(error_message)
        return stats

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

    await client.start()

    await join_channel(client, channel_username)

    print(Fore.CYAN + "Scraping messages and media...")
    stats = await scrape_messages_and_media(client, channel_username, text_dir, media_dir, limit=None)

    await client.disconnect()  # Disconnect the client when done

    # Provide a summary to the user
    print(Fore.GREEN + "\nScraping Completed!")
    print(Fore.GREEN + f"Total messages scraped: {stats['messages']}")
    print(Fore.GREEN + f"Messages saved to: {os.path.abspath(os.path.join(text_dir, 'messages.txt'))}")

    if stats['media']:
        print(Fore.GREEN + "\nMedia files downloaded:")
        for media_type, count in stats['media'].items():
            print(Fore.GREEN + f"  {media_type.capitalize()}s: {count}")
        print(Fore.GREEN + f"Media files saved to: {os.path.abspath(media_dir)}")
    else:
        print(Fore.GREEN + "No media files were downloaded.")

if __name__ == '__main__':
    asyncio.run(main())
