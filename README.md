# Telegram Chat Summarizer

A powerful tool for lazy developers who want to automatically fetch and summarize their Telegram chats using local AI models. This application exports chat messages and generates intelligent summaries that filter out casual talk and focus on important information.

## Features

- **Smart AI Summarization**: Uses Ollama models to generate focused summaries
- **Intelligent Filtering**: Automatically ignores casual talk, memes, and irrelevant chatter
- **Local Processing**: All data stays on your machine - no cloud services used
- **Multiple Scripts**: Choose from basic export to full AI-powered summarization
- **Easy Setup**: Simple configuration with automatic model detection
- **Privacy First**: Your messages never leave your computer

## Quick Start

### Prerequisites

1. **Ollama installed and running**:
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull a model (recommended for summarization)
   ollama pull llama3.2:3b
   ```

2. **Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Telegram API credentials**:
   - Visit https://my.telegram.org/auth
   - Go to 'API Development Tools'
   - Create a new application
   - Get your `api_id`, `api_hash`, and `username`

### Basic Usage

```bash
# Run the recommended version with AI summarization
python working_prototype_2.py
```

## Available Scripts

### 1. `working_prototype_2.py` (Recommended)
**Best choice for most users** - Simple, reliable, and includes intelligent AI summarization.

**Features:**
- Based on the working prototype
- Automatic Ollama model detection
- Generates `summary.txt` as requested
- **Smart filtering**: Ignores trash talk, memes, casual chatter
- **Focused summaries**: Only important decisions and information
- Clean, professional interface
- Robust error handling

**Usage:**
```bash
python working_prototype_2.py
```

### 2. `working_prototype.py` (Original)
**Basic version** - Exports chats to text files without AI summarization.

**Features:**
- Simple and reliable
- Exports chat to `.txt` file
- No AI summarization

**Usage:**
```bash
python working_prototype.py
```

### 3. `main.py` (Full-featured)
**Advanced version** - Feature-rich with enhanced UI and error handling.

**Features:**
- Enhanced user interface
- Automatic Ollama management
- Generates `summary.txt`
- Comprehensive error handling
- Model auto-download

**Usage:**
```bash
python main.py
```

## Configuration

### First Run Setup
1. Run any of the scripts
2. Enter your Telegram API credentials when prompted:
   - API ID
   - API Hash  
   - Username (without @)
3. Complete Telegram authentication (one-time setup)

### Config File
Credentials are saved in `config.ini`:
```ini
[Telegram]
api_id = your_api_id
api_hash = your_api_hash
username = your_username
```

## Ollama Models

The scripts automatically detect and use the best available model. Recommended models for summarization:

**Best Performance:**
- `llama3.1:70b` (requires powerful hardware)
- `llama3.1:8b` (good balance)

**Recommended for most users:**
- `llama3.2:3b` (fast, efficient)
- `llama3:7b` (good quality)

**Install a model:**
```bash
ollama pull llama3.2:3b
```

## Output Files

### Chat Export
- **Filename**: `{chat_name}_export_{date}.txt`
- **Content**: Chronological chat messages with timestamps and sender names

### Summary
- **Filename**: `summary.txt` (overwrites previous summaries)
- **Content**: AI-generated summary with metadata including:
  - Generation timestamp
  - Model used
  - Source file
  - **Intelligent filtering**: Automatically ignores casual talk, memes, greetings
  - **Focused content**: Only includes important decisions, action items, and key information
  - **Structured format**: Organized bullet points under relevant categories

## Troubleshooting

### Common Issues

**1. "Ollama service is not running"**
```bash
# Start Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

**2. "No Ollama models found"**
```bash
# Install a model
ollama pull llama3.2:3b

# List installed models
ollama list
```

**3. "Failed to connect to Telegram"**
- Check internet connection
- Verify API credentials in `config.ini`
- Ensure credentials are not empty

**4. "Request timed out"**
- Model might be too large for your hardware
- Try a smaller model: `ollama pull llama3.2:3b`
- Increase timeout in the script if needed

### Performance Tips

**For faster summarization:**
- Use smaller models (`llama3.2:3b`, `phi3:3.8b`)
- Limit message count (100-500 messages)
- Ensure sufficient RAM for the model

**For better quality:**
- Use larger models (`llama3.1:8b`, `llama3:7b`)
- Allow more time for generation
- Use more recent/specific models

## Privacy & Security

- **Local Processing**: All data stays on your machine
- **No Cloud Services**: Ollama runs locally
- **Credential Storage**: API credentials stored locally in `config.ini`
- **Session Management**: Telegram session cached locally for convenience

## Example Workflow

1. **Setup** (one-time):
   ```bash
   ollama serve
   ollama pull llama3.2:3b
   pip install -r requirements.txt
   ```

2. **Run summarizer**:
   ```bash
   python working_prototype_2.py
   ```

3. **Follow prompts**:
   - Enter API credentials (first time only)
   - Select chat from list
   - Choose number of messages (default: 100)

4. **Get results**:
   - `{chat_name}_export_{date}.txt` - Full chat export
   - `summary.txt` - AI-generated summary

## Recommendations

- **For beginners**: Use `working_prototype_2.py`
- **For basic export only**: Use `working_prototype.py`  
- **For advanced features**: Use `main.py`
- **Model choice**: Start with `llama3.2:3b` for speed, upgrade to `llama3.1:8b` for quality
- **Message limit**: 100-500 messages for best balance of context and speed

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Verify Ollama is running: `ollama list`
3. Check Python dependencies: `pip install -r requirements.txt`
4. Ensure config.ini has valid credentials
5. Try with a smaller model or fewer messages

## License

No license