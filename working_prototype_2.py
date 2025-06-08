from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
import datetime
import asyncio
import os
import configparser
import requests
import json

def get_best_ollama_model():
    """Get the best available Ollama model from the installed models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print("ERROR: Ollama service is not running. Please start it with 'ollama serve'")
            return None
            
        models = response.json().get("models", [])
        if not models:
            print("ERROR: No Ollama models found. Please install a model first (e.g., 'ollama pull llama3.2:3b')")
            return None
        
        # Priority list of preferred models for summarization (best to worst)
        preferred_models = [
            "llama3.1:70b", "llama3.1:8b", "llama3.2:3b", "llama3:8b", "llama3:7b",
            "mistral:7b", "codellama:7b", "deepseek-r1:latest", "qwen2:7b",
            "gemma:7b", "phi3:3.8b", "tinyllama:1.1b"
        ]
        
        available_models = [model["name"] for model in models]
        print(f"Available Ollama models: {', '.join(available_models)}")
        
        # Find the best available model
        for preferred in preferred_models:
            if preferred in available_models:
                print(f"Selected model: {preferred}")
                return preferred
        
        # If no preferred model found, use the first available
        selected = available_models[0]
        print(f"Selected model: {selected} (first available)")
        return selected
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Ollama. Make sure Ollama is running with 'ollama serve'")
        return None
    except Exception as e:
        print(f"ERROR: Error getting Ollama models: {str(e)}")
        return None

def generate_summary_with_ollama(input_file, model_name):
    """Generate summary using Ollama model"""
    print(f"\nINFO: Generating summary using {model_name}...")
    
    try:
        # Read the content of the file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limit content to avoid token limits (most models handle ~4k tokens well)
        max_chars = 15000  # Roughly 3-4k tokens
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[Content truncated due to length...]"
            print(f"WARNING: Content truncated to {max_chars} characters to fit model limits")
        
        # Create a focused prompt for summarization
        prompt = f"""Analyze the following Telegram chat conversation and provide a concise summary that focuses ONLY on important information. 

IGNORE:
- Casual greetings, small talk, jokes, memes
- Off-topic discussions, random chatter
- Repetitive messages or spam
- Personal conversations not relevant to main topics

INCLUDE ONLY:
- Important decisions made
- Key information shared (facts, data, announcements)
- Action items and deadlines
- Problem discussions and solutions
- Meeting schedules and important events
- Technical discussions and conclusions
- Business/work-related updates

Format the summary as bullet points under relevant categories. If there's nothing important to summarize, just say "No significant information found in this conversation."

Conversation:
{content}

Important Summary:"""
        
        # Send request to Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Lower temperature for more focused summaries
                    "top_p": 0.8,        # More focused token selection
                    "num_predict": 800,  # Limit response length for conciseness
                    "repeat_penalty": 1.1  # Avoid repetition
                }
            },
            timeout=120  # 2 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get("response", "").strip()
            
            if not summary:
                print("ERROR: Model returned empty response")
                return None
            
            # Write summary to summary.txt
            summary_file = "summary.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Chat Summary Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model Used: {model_name}\n")
                f.write(f"Source File: {input_file}\n")
                f.write("="*80 + "\n\n")
                f.write(summary)
                f.write("\n\n" + "="*80)
            
            print(f"SUCCESS: Summary generated and saved to {summary_file}")
            
            # Display the summary
            print("\n" + "="*80)
            print(" "*30 + "CHAT SUMMARY")
            print("="*80)
            print(summary)
            print("="*80)
            
            return summary_file
        else:
            print(f"ERROR: Failed to generate summary. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out. The model might be too slow or overloaded.")
        return None
    except Exception as e:
        print(f"ERROR: Error generating summary: {str(e)}")
        return None

config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    config['Telegram'] = {
        'api_id': '', # Enter your Telegram API ID
        'api_hash': '', # Enter your Telegram API Hash
        'username': '' # Enter your Telegram username
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
    # Check if Ollama is available and get the best model
    model_name = get_best_ollama_model()
    if not model_name:
        print("\nERROR: Cannot proceed without a working Ollama setup.")
        print("Please ensure:")
        print("1. Ollama is installed and running ('ollama serve')")
        print("2. At least one model is installed ('ollama pull llama3.2:3b')")
        return
    
    await client.start()
    dialogs = await client.get_dialogs()
    print("\nAvailable chats:")
    for i, dialog in enumerate(dialogs):
        print(f"{i}: {dialog.name} ({dialog.id})")
    choice = int(input("Enter the number of the chat to summarize: "))
    chat = dialogs[choice]
    print(f"Selected chat: {chat.name}")
    limit = int(input("How many recent messages to fetch (default 100): ") or "100")
    print(f"Fetching the {limit} most recent messages...")
    messages = await client.get_messages(chat, limit=limit)

    filename = f"{chat.name.replace(' ', '_')}_export_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Chat Export from {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for message in reversed(messages): #oldest first
            if message.text:
                sender = message.sender.first_name if hasattr(message.sender, 'first_name') else "Unknown"
                date = message.date.strftime('%Y-%m-%d %H:%M')
                f.write(f"[{date}] {sender}: {message.text}\n\n")

    print(f"\nSUCCESS: Chat exported to: {filename}")
    
    # Generate summary using Ollama
    summary_file = generate_summary_with_ollama(filename, model_name)
    
    if summary_file:
        print(f"\nSUCCESS: Process completed successfully!")
        print(f"INFO: Original chat: {filename}")
        print(f"INFO: Summary: {summary_file}")
    else:
        print(f"\nWARNING: Chat exported but summary generation failed.")
        print(f"You can still use the exported file '{filename}' with your preferred LLM")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())