#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "   WELCOME TO THE SUPER LAZY TELEGRAM CHAT SUMMARIZER"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "This tool will help you summarize your Telegram chats"
echo "without you having to do much work at all."
echo ""
echo "Using host's Ollama instance (http://host.docker.internal:11434)..."

# Modify the Python script to use the host's Ollama instance
sed -i 's|"http://localhost:11434/api|"http://host.docker.internal:11434/api|g' main.py

python main.py

# Keep container running if needed for debugging
if [ "$1" = "keep-alive" ]; then
  tail -f /dev/null
fi