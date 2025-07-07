import asyncio
import os
from dotenv import load_dotenv
import tweepy
from agents import Agent, Runner, FunctionTool
from pydantic import BaseModel
import json
from youtube_transcript_api import YouTubeTranscriptApi

# Constants
DEFAULT_VIDEO_LINK = "https://www.youtube.com/watch?v=u5-UMgNZs6k"

def create_prompt(video_url):
    return f"""
You are a marketing agent that processes YouTube videos and creates viral tweets.

WORKFLOW - Execute these steps in order:

1. **STEP 1 - Get Video Content**: Use the youtube_summary_tool to fetch the transcript from {video_url}
   - Call: youtube_summary_tool with video_url parameter
   
2. **STEP 2 - Create Tweet**: Based on the transcript, create a compelling tweet that:
   - Is under 280 characters
   - Has viral potential
   - Includes engaging content from the video
   
3. **STEP 3 - Post Tweet**: You MUST hand off to the "Twitter Posting Agent" to post the tweet
   - Transfer control to the Twitter Posting Agent
   - The Twitter agent will handle the actual posting

CRITICAL: After creating the tweet, you MUST hand off to the Twitter Posting Agent. Do not stop after creating the tweet content.

Target video: {video_url}
"""

class TweetArgs(BaseModel):
    tweet: str

class YouTubeSummaryArgs(BaseModel):
    video_url: str

def get_video_transcript(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'ko'])
    transcript = ' '.join([i['text'] for i in transcript_raw])
    return transcript

async def summarize_youtube_video(context, args):
    print("YouTube summary function called with args:", args)
    
    if isinstance(args, str):
        try:
            args_dict = json.loads(args)
            video_url = args_dict.get('video_url', DEFAULT_VIDEO_LINK)
        except (json.JSONDecodeError, AttributeError):
            video_url = DEFAULT_VIDEO_LINK
    else:
        video_url = args.video_url if hasattr(args, 'video_url') else DEFAULT_VIDEO_LINK
    
    print(f"Fetching transcript for: {video_url}")
    
    try:
        transcript = get_video_transcript(video_url)
        print(f"Transcript fetched successfully! Length: {len(transcript)} characters")
        return {"summary": transcript, "video_url": video_url}
    except Exception as e:
        print(f"Failed to get transcript: {e}")
        return {"error": f"Failed to get video transcript: {str(e)}", "video_url": video_url}

async def make_tweet(context, args):
    print("Tweet function called with args:", args)
    
    # Handle both string and TweetArgs object inputs
    if isinstance(args, str):
        try:
            args_dict = json.loads(args)
            tweet = args_dict.get('tweet', args)
        except (json.JSONDecodeError, AttributeError):
            tweet = args
    elif hasattr(args, 'tweet'):
        tweet = args.tweet
    else:
        tweet = str(args)
    
    print(f"Attempting to post tweet: {tweet}")
    
    try:
        twitter_client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
            consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            wait_on_rate_limit=True
        )
        
        response = twitter_client.create_tweet(text=tweet)
        print(f"Tweet posted successfully! ID: {response.data['id']}")
        return {"status": "success", "tweet": response.data["text"], "tweet_id": response.data["id"]}
    except Exception as e:
        print(f"Failed to post tweet: {e}")
        return {"status": "error", "message": f"Failed to post tweet: {str(e)}"}

# Define Tools
youtube_summary_tool = FunctionTool(
    name="youtube_summary_tool",
    description="Fetches and summarizes a YouTube video based on its URL.",
    params_json_schema=YouTubeSummaryArgs.model_json_schema(),
    on_invoke_tool=summarize_youtube_video
)

tweet_tool = FunctionTool(
    name="tweet_tool",
    description="Posts a tweet on Twitter.",
    params_json_schema=TweetArgs.model_json_schema(),
    on_invoke_tool=make_tweet
)

# Define Agents
twitter_agent = Agent(
    name="Twitter Posting Agent",
    model="litellm/gemini/gemini-2.0-flash",
    instructions="""You are a Twitter posting specialist.

When you receive a handoff with tweet content:
1. Extract the tweet text from the previous conversation
2. Use the tweet_tool to post it immediately 
3. Confirm the tweet was posted successfully
4. Keep tweet content concise and engaging, do not include emojies.
5. Keep it HUMAN-LIKE.

Call tweet_tool with format: {"tweet": "the tweet content here"}

Post the tweet now!""",
    tools=[tweet_tool]
)

def create_host_agent(video_url):
    return Agent(
        name="Marketing Agent",
        model="litellm/gemini/gemini-2.0-flash",
        instructions=create_prompt(video_url),
        tools=[youtube_summary_tool],
        handoffs=[twitter_agent]
    )

async def main(video_url=None):
    try:
        load_dotenv()
        
        if video_url is None:
            video_url = DEFAULT_VIDEO_LINK
        
        print(f"Processing video: {video_url}")
        
        host_agent = create_host_agent(video_url)
        
        print("Starting agent workflow...")
        result = await Runner.run(
            host_agent,
            f"""Process this YouTube video: {video_url}

MANDATORY STEPS:
1. Use youtube_summary_tool to get the video transcript
2. Create a viral tweet based on the content
3. MUST hand off to Twitter Posting Agent to post the tweet

DO NOT STOP until you have handed off to the Twitter Posting Agent and the tweet is posted!"""
        )
        
        print("Workflow completed!")
        print(f"Final Result: {result}")
        
        # Check if tweet was actually posted by looking at the result
        if "Twitter Posting Agent" in str(result):
            print("✅ Tweet was posted successfully!")
        else:
            print("⚠️ Warning: Handoff to Twitter agent may not have occurred")
            
        return result
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())