#!/bin/bash

ollama serve &

# Wait a bit for Ollama to start
sleep 3

echo "════════════════════════════════════════════════════════════"
echo "   WELCOME TO THE SUPER LAZY TELEGRAM CHAT SUMMARIZER"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "This tool will help you summarize your Telegram chats"
echo "without you having to do much work at all."
echo ""
echo "Starting up services..."

python main.py

# Keep container running if needed for debugging
if [ "$1" = "keep-alive" ]; then
  tail -f /dev/null
fi