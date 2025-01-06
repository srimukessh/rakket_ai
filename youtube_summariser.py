from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic_ai import Agent, Tool, RunContext
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))

def get_video_details(video_id):
    """Fetch video details from YouTube API."""
    response = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    ).execute()
    
    item = response.get("items", [])[0]
    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "duration": item["contentDetails"]["duration"],
        "tags": item["snippet"].get("tags", [])
    }

def fetch_subtitles(video_id):
    """Fetch video subtitles using YouTube Transcript API."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = " ".join([item['text'] for item in transcript])
        return subtitles
    except Exception as e:
        return f"Error fetching subtitles: {e}"

def prepare_text_for_llm(video_id):
    """Combine video subtitles and description."""
    subtitles = fetch_subtitles(video_id)
    description = get_video_details(video_id).get("description", "")
    return f"Subtitles:\n{subtitles}\n\nDescription:\n{description}"

# Define the summarization tool
def summarize_text(ctx: RunContext[str], content: str) -> str:
    """Summarize the given content."""
    return f"Summarize this text: {content}"

# Create AI agent
agent = Agent(
    model='gemini-1.5-flash',
    system_prompt=(
        "You are a tennis coach who summarizes tennis-related content. "
        "When summarizing, focus on key tennis techniques, drills, and coaching points "
        "in a clear, professional manner."
    ),
    tools=[Tool(summarize_text, description="Summarize the given text.")]
)

async def summarize_video(video_id: str):
    """Main function to process video and get summary."""
    try:
        # Prepare text from video
        combined_text = prepare_text_for_llm(video_id)
        
        # Get AI summary
        result = await agent.run(combined_text)
        return result.data
        
    except Exception as e:
        return f"Error processing video: {e}"

# Function to run the async code
def get_video_summary(video_id: str):
    """Wrapper function to run async code."""
    return asyncio.run(summarize_video(video_id))

if __name__ == "__main__":
    # Example usage
    video_id = input("Enter YouTube video ID: ")
    summary = get_video_summary(video_id)
    print("\nSummary:")
    print(summary) 