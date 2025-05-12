# Super Lazy Telegram Chat Summarizer

A Docker-based application for people who are too lazy to summarize their Telegram chats. This tool automatically fetches your Telegram chats and summarizes them using the DeepSeek-R1 AI model.

## Features

-  One-command setup with Docker
-  Access to all your Telegram chats
-  AI-powered chat summarization with DeepSeek-R1
-  Your data stays local - no cloud services used

## Prerequisites

- Docker installed on your system
- A Telegram account
- API credentials from Telegram (the app will show you how to get these)

## Quick Start for Super Lazy People

### Step 1: Pull and run the Docker image

```bash
docker run -it --name telegram-summarizer telegram-summarizer
```

### Step 2: Follow the prompts

1. The app will show you how to get your Telegram API credentials
2. Enter your API ID, API hash, and username when prompted
3. Select a chat to summarize
4. Enter how many messages to fetch
5. Wait for the summary to be generated

That's it! You'll get a nicely formatted summary of your chat without having to read through everything.

## Building from Source

If you want to build the Docker image yourself:

```bash
# Clone this repository
git clone https://github.com/yourusername/telegram-summarizer.git
cd telegram-summarizer

# Build the Docker image
docker build -t telegram-summarizer .

# Run the container
docker run -it --name telegram-summarizer telegram-summarizer
```

## First Time Setup

When you run the application for the first time:

1. You'll need to authenticate with Telegram via a code sent to your account
2. This only happens once - your session is saved for future use
3. Your API credentials are stored locally in the Docker container

## Troubleshooting

- **Connection issues**: Make sure your internet connection is stable
- **API errors**: Double-check your Telegram API credentials
- **Container crashes**: Run with `docker run -it --name telegram-summarizer telegram-summarizer keep-alive` for debugging

## Privacy Note

This application runs completely on your local machine. Your Telegram messages and API credentials never leave your computer. The DeepSeek-R1 model runs locally within the Docker container.

## Original Code (before AI transformation) (Give this a try as well, here local LLM is not used)
```python
from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
import datetime
import asyncio
import os
import configparser

config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    config['Telegram'] = {
        'api_id': '', # Fill this mf
        'api_hash': '', # Fill this mf also
        'username': '' # Still need to fill this mf
    }
    
    with open('config.ini', 'w') as f:
        config.write(f)
    print("Created config.ini - please fill in your API credentials")
    exit()
else:
    config.read('config.ini')
    
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

async def main():
    await client.start()
    dialogs = await client.get_dialogs()
    print("available chats:")
    for i, dialog in enumerate(dialogs):
        print(f"{i}: {dialog.name} ({dialog.id})")
    choice = int(input("Enter the number of the chat to summarize: "))
    chat = dialogs[choice]
    print(f"selected chat: {chat.name}")
    limit = int(input("How many recent messages to fetch (default 100): ") or "100")
    print(f"fetching the {limit} most recent messages...")
    messages = await client.get_messages(chat, limit=limit)

    filename = f"{chat.name.replace(' ', '_')}_export_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Chat Export from {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for message in reversed(messages): #oldes first
            if message.text:
                sender = message.sender.first_name if hasattr(message.sender, 'first_name') else "Unknown"
                date = message.date.strftime('%Y-%m-%d %H:%M')
                f.write(f"[{date}] {sender}: {message.text}\n\n")

    print(f"\nNext steps:")
    print(f"1. Use the exported file '{filename}' with your preferred LLM")
    print(f"2. For example: 'claude summarize {filename}'")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## License

No license