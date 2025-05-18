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