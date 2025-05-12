''' 
    Developer: LLM
    Date: 2023-10-01
    License: None
    Current Status: In Progress(Prototype is not working)
    
    Description:
    This script is a Telegram chat summarizer that uses the Ollama deepseek-r1 model.
    Script is just a transformation of the original script (Available in README.md)
    which is entirely created by LLM and is not a copy of any other script.
    The script is a Telegram chat summarizer that uses the Ollama deepseek-r1 model.
    It connects to the Telegram API, fetches messages from a selected chat,
    and generates a summary using the deepseek-r1 model.
    The script is designed to be user-friendly and requires minimal input from the user.
'''

from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
import datetime
import asyncio
import os
import configparser
import requests
import time
import textwrap
import subprocess
import sys

def print_user_guide():
    guide = """
╔════════════════════════════════════════════════════════════════════════╗
║                       TELEGRAM CHAT SUMMARIZER                          ║
║                  FOR SUPER LAZY PEOPLE - USER GUIDE                     ║
╚════════════════════════════════════════════════════════════════════════╝

To use this application, you need to provide your Telegram API credentials.
Here's how to get them:

1. Visit https://my.telegram.org/auth and log in with your phone number
2. Go to 'API Development Tools'
3. Create a new application with any name and short name
4. Copy the 'App api_id' and 'App api_hash' values
5. You'll also need your Telegram username (without the '@' symbol)

These credentials will allow this app to access your Telegram chats.
Don't worry - your credentials stay on your device and are only used
to access your own chats.

For more detailed instructions, visit:
https://core.telegram.org/api/obtaining_api_id
    """
    print(guide)

config = configparser.ConfigParser()

# First run check to see if we need to create config
if not os.path.exists('config.ini') or os.path.getsize('config.ini') == 0:
    print_user_guide()
    
    api_id = input("\nEnter your Telegram API ID: ").strip()
    api_hash = input("Enter your Telegram API hash: ").strip()
    username = input("Enter your Telegram username (without @): ").strip()
    
    config['Telegram'] = {
        'api_id': api_id,
        'api_hash': api_hash,
        'username': username
    }
    
    with open('config.ini', 'w') as f:
        config.write(f)
    print("\nCredentials saved to config.ini")
else:
    config.read('config.ini')
    
    # Check if any values are empty
    if not all([config['Telegram']['api_id'], config['Telegram']['api_hash'], config['Telegram']['username']]):
        print("Config file exists but contains empty values. Let's update it.")
        print_user_guide()
        
        api_id = input("\nEnter your Telegram API ID: ").strip() or config['Telegram']['api_id']
        api_hash = input("Enter your Telegram API hash: ").strip() or config['Telegram']['api_hash']
        username = input("Enter your Telegram username (without @): ").strip() or config['Telegram']['username']
        
        config['Telegram'] = {
            'api_id': api_id,
            'api_hash': api_hash,
            'username': username
        }
        
        with open('config.ini', 'w') as f:
            config.write(f)
        print("\nCredentials updated in config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# Check if Ollama is running and start it if needed
def ensure_ollama_running():
    """Check if Ollama is running, and start it if not"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        # If we get here, Ollama is running
        print("✓ Ollama service is running")
    except requests.exceptions.ConnectionError:
        print("Starting Ollama service...")
        # Start Ollama in the background
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        # Give it some time to start
        max_retries = 10
        for i in range(max_retries):
            print(f"Waiting for Ollama to start ({i+1}/{max_retries})...")
            time.sleep(3)
            try:
                requests.get("http://localhost:11434/api/tags")
                print("✓ Ollama service started successfully")
                break
            except requests.exceptions.ConnectionError:
                if i == max_retries - 1:
                    print("❌ Failed to start Ollama service. Please check your installation.")
                    sys.exit(1)

def ensure_model_pulled():
    """Make sure the deepseek-r1 model is downloaded"""
    print("Checking for deepseek-r1 model...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get("models", [])
        model_names = [model.get("name") for model in models]
        
        if "deepseek-r1:latest" not in model_names:
            print("Downloading deepseek-r1 model (this may take a while)...")
            subprocess.run(["ollama", "pull", "deepseek-r1:latest"], check=True)
            print("✓ deepseek-r1 model downloaded successfully")
        else:
            print("✓ deepseek-r1 model is already downloaded")
    except Exception as e:
        print(f"❌ Error checking/pulling the model: {str(e)}")
        sys.exit(1)

def generate_summary(input_file):
    """Use Ollama with deepseek-r1 to summarize the text file"""
    print("\n🤖 Generating summary with DeepSeek-R1 model...")
    
    try:
        # Read the content of the file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Define the prompt for summarization
        prompt = f"""
        Please provide a concise summary of the following Telegram chat conversation.
        Focus on the main topics discussed, key decisions made, and important information shared.
        
        The summary should be well-structured and highlight what's most important.
        
        --- CONVERSATION START ---
        {content[:50000]}  # Limit to 50k chars to avoid token limits
        --- CONVERSATION END ---
        """
        
        # Send request to Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            summary = response.json().get("response", "")
            
            # Write summary to file
            summary_file = input_file.replace(".txt", "_summary.txt")
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"\n✅ Summary generated and saved to {summary_file}")
            
            # Print the summary with nice formatting
            print("\n" + "="*80)
            print(" "*30 + "SUMMARY")
            print("="*80 + "\n")
            
            # Print with word wrapping
            for line in summary.split('\n'):
                print('\n'.join(textwrap.wrap(line, width=80)))
                
            print("\n" + "="*80)
            return summary_file
        else:
            print(f"❌ Failed to generate summary: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating summary: {str(e)}")
        return None

client = TelegramClient(username, api_id, api_hash)

async def get_chat_list():
    """Get a list of all dialogs (chats) and let user select one"""
    dialogs = await client.get_dialogs()
    
    print("\n📱 Available Telegram Chats:")
    print("-" * 60)
    for i, dialog in enumerate(dialogs[:30]):  # Limit to first 30 for clarity
        dialog_type = "👤 Private" if dialog.is_user else "👥 Group" if dialog.is_group else "📢 Channel"
        print(f"{i}: {dialog_type} | {dialog.name} (ID: {dialog.id})")
    
    while True:
        try:
            choice = input("\nEnter the number of the chat to summarize: ")
            choice = int(choice)
            if 0 <= choice < len(dialogs):
                return dialogs[choice]
            else:
                print(f"❌ Please enter a number between 0 and {len(dialogs)-1}")
        except ValueError:
            print("❌ Please enter a valid number")

async def get_messages(chat, limit=100):
    """Get messages from a specific chat"""
    print(f"\n⏳ Fetching the {limit} most recent messages from '{chat.name}'...")
    messages = await client.get_messages(chat, limit=limit)
    print(f"✓ Successfully retrieved {len(messages)} messages")
    return messages

async def export_to_text(messages, filename):
    """Export messages to a text file"""
    print(f"\n📝 Exporting messages to {filename}...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Chat Export from {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Chat: {messages[0].chat.title if hasattr(messages[0].chat, 'title') else 'Private Chat'}\n\n")
        
        message_count = 0
        for message in reversed(messages):  # oldest first
            if message.text:
                sender = message.sender.first_name if hasattr(message.sender, 'first_name') and message.sender else "Unknown"
                date = message.date.strftime('%Y-%m-%d %H:%M')
                f.write(f"[{date}] {sender}: {message.text}\n\n")
                message_count += 1
    
    print(f"✓ Successfully exported {message_count} messages with text content")
    return filename

async def main():
    # Check and start Ollama if needed
    ensure_ollama_running()
    ensure_model_pulled()
    
    # Connect to Telegram
    print("\n🔄 Connecting to Telegram...")
    try:
        await client.start()
        print("✓ Successfully connected to Telegram")
    except Exception as e:
        print(f"❌ Failed to connect to Telegram: {str(e)}")
        print("  Check your internet connection and API credentials")
        return
    
    try:
        # Select chat and fetch messages
        chat = await get_chat_list()
        
        while True:
            try:
                limit_input = input("\nHow many recent messages to fetch (default 100): ").strip()
                limit = int(limit_input) if limit_input else 100
                if limit <= 0:
                    print("❌ Please enter a positive number")
                    continue
                if limit > 1000:
                    confirm = input("⚠️ Fetching more than 1000 messages may be slow. Continue? (y/n): ").lower()
                    if confirm != 'y':
                        continue
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        messages = await get_messages(chat, limit=limit)
        
        if not messages:
            print("❌ No messages found in this chat")
            return
            
        # Generate safe filename from chat name
        safe_name = ''.join(c if c.isalnum() else '_' for c in chat.name)
        filename = f"{safe_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        # Export messages to file
        exported_file = await export_to_text(messages, filename)
        
        # Generate summary using Ollama
        summary_file = generate_summary(exported_file)
        
        print("\n🎉 All done! You didn't have to do much, did you?")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    finally:
        await client.disconnect()
        print("\n👋 Disconnected from Telegram")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unhandled error: {str(e)}")