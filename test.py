import asyncio
import os
from dotenv import load_dotenv
import tweepy
from agents import Agent, Runner, FunctionTool
from pydantic import BaseModel
import json
import requests
from youtube_transcript_api import YouTubeTranscriptApi

# agent = Agent(
#     name="YouTube Video Summarizer",
#     model="litellm/gemini/gemini-2.5-flash",
#     instructions="""You are an expert YouTube video analyzer and summarizer in just one sentence.""",
# )

# async def main():
#     try:
#         # Initialize environment variables
#         load_dotenv()

#         # Run the agent with the task
#         result = await Runner.run(
#             agent,
#             "Summarize the YouTube video at https://www.youtube.com/watch?v=u5-UMgNZs6k"
#         )
#         print(result)
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())

url = "https://www.youtube.com/watch?v=u5-UMgNZs6k"
video_id = url.split("v=")[-1].split("&")[0]

transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'ko'])
transcript_full = ' '.join([i['text'] for i in transcript_raw])
print(transcript_full)
