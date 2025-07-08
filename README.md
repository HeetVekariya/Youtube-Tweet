# YouTube-Tweet Automation

An automated system that processes YouTube videos and creates viral tweets using AI agents. This project extracts video transcripts, generates engaging tweet content, and automatically posts them to Twitter.

## Blog Tutorial

Follow along with the detailed blog post: [Automate Tweets from YouTube Videos](https://dev.to/heetvekariya/automate-tweets-from-youtube-videos-7hh)

## Features

- **YouTube Transcript Extraction**: Automatically fetches video transcripts from YouTube videos
- **AI-Powered Tweet Generation**: Uses Gemini AI to create viral, engaging tweets from video content
- **Automatic Twitter Posting**: Posts generated tweets directly to your Twitter account
- **Multi-Agent System**: Coordinated workflow between Marketing Agent and Twitter Posting Agent
- **Error Handling**: Robust error handling for API calls and network issues

## Technologies Used

- **Python 3.10+**
- **OpenAI Agents**: Multi-agent framework for coordinated AI workflows
- **Tweepy**: Twitter API integration
- **YouTube Transcript API**: For extracting video transcripts
- **Gemini AI**: For content generation
- **Python-dotenv**: Environment variable management

## Prerequisites

Before running this project, make sure you have:

1. **Python 3.10 or higher** installed
2. **Twitter Developer Account** with API keys
3. **Google AI Studio Account** for Gemini API access
4. **UV package manager** (recommended) or pip

## Installation

1. Clone the repository:
```bash
https://github.com/HeetVekariya/Youtube-Tweet.git
cd YouTube-Tweet
```

2. Install dependencies using UV:
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Fill in your API credentials in the `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

## Usage

### Basic Usage

Run the script with the default video:
```bash
python main.py
```

### Custom Video URL

You can modify the `DEFAULT_VIDEO_LINK` variable in `main.py` or pass a custom URL programmatically.

### How It Works

1. **Video Processing**: The Marketing Agent fetches the YouTube video transcript
2. **Content Generation**: AI analyzes the transcript and creates an engaging tweet (under 280 characters)
3. **Tweet Posting**: The Twitter Posting Agent handles the actual posting to your Twitter account
4. **Verification**: The system confirms successful posting and provides feedback

## Project Structure

```
YouTube-Tweet/
├── main.py              # Main application logic
├── test.py              # Test file
├── pyproject.toml       # Project configuration
├── .env.example         # Environment variables template
├── .env                 # Your API credentials (not tracked)
├── uv.lock              # UV lock file
└── README.md            # This file
```

## API Keys Setup

### Twitter API Keys

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Generate your API keys and tokens
4. Add them to your `.env` file

### Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project
3. Generate an API key
4. Add it to your `.env` file

## Agent Workflow

The system uses a coordinated multi-agent approach:

1. **Marketing Agent**: 
   - Fetches YouTube video transcripts
   - Analyzes content for viral potential
   - Creates engaging tweet content
   - Hands off to Twitter Posting Agent

2. **Twitter Posting Agent**:
   - Receives tweet content from Marketing Agent
   - Posts the tweet to Twitter
   - Confirms successful posting

## Error Handling

The system includes comprehensive error handling for:
- Invalid YouTube URLs
- API rate limits
- Network connectivity issues
- Missing or invalid API credentials
- Tweet posting failures

## Example Output

```
Processing video: https://www.youtube.com/watch?v=example
Starting agent workflow...
YouTube summary function called with args: {'video_url': 'https://www.youtube.com/watch?v=example'}
Fetching transcript for: https://www.youtube.com/watch?v=example
Transcript fetched successfully! Length: 5240 characters
Tweet function called with args: {'tweet': 'Your generated tweet content here'}
Tweet posted successfully! ID: 1234567890
✅ Tweet was posted successfully!
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

- OpenAI Agents framework for multi-agent coordination
- YouTube Transcript API for video content extraction
- Tweepy for Twitter integration
- Google's Gemini AI for content generation

---

For detailed implementation guide and tutorials, check out the [blog post](https://dev.to/heetvekariya/automate-tweets-from-youtube-videos-7hh).