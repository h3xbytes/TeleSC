# Telegram Channel Scraper

This script allows you to scrape messages and media from a Telegram channel.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
  - [Obtain Telegram API Credentials](#1-obtain-telegram-api-credentials)
  - [Set Up Environment Variables](#2-set-up-environment-variables)
  - [Install Dependencies](#3-install-dependencies)
- [Running the Script](#running-the-script)
- [Authentication Process](#authentication-process)
  - [Entering Your Phone Number](#entering-your-phone-number)
  - [Entering the Telegram Code](#entering-the-telegram-code)
- [Building an Executable](#building-an-executable)
- [Important Notes](#important-notes)
- [Disclaimer](#disclaimer)

## Requirements

- **Python 3.7** or higher
- **Telegram API credentials** (API ID and API Hash)
- **Telegram account** (with access to the target channel)

## Setup

### 1. Obtain Telegram API Credentials

- Go to [my.telegram.org](https://my.telegram.org/) and log in with your Telegram account.
- Click on **API development tools**.
- Fill in the required details to get your **API ID** and **API Hash**.

### 2. Set Up Environment Variables

#### Option A: Using a `.env` File (Recommended)

- Create a file named `.env` in the project directory.
- Add your API credentials to the file:

  ```ini
  TELEGRAM_API_ID=your_api_id
  TELEGRAM_API_HASH=your_api_hash
