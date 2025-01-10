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

# Create AI agent with more specific instructions
agent = Agent(
    model='gemini-1.5-flash',
    system_prompt=(
        "You are a tennis coach who provides detailed, structured summaries of tennis videos. "
        "For each video:\n"
        "1. Summarize the main topic and target audience\n"
        "2. Break down each drill or technique mentioned\n"
        "3. Include specific technical details and coaching points\n"
        "4. Organize the information in clear sections\n"
        "Format the output with proper spacing and bullet points for readability."
    ),
    tools=[Tool(summarize_text, description="Summarize the given text.")]
)

async def summarize_video(video_id: str):
    """Main function to process video and get summary."""
    try:
        combined_text = prepare_text_for_llm(video_id)
        print(f"Text length: {len(combined_text)}")  # Debug log
        
        result = await agent.run(combined_text)
        print(f"Response length: {len(result.data)}")  # Debug log
        
        return result.data
        
    except Exception as e:
        print(f"Error details: {str(e)}")  # Debug log
        return f"Error processing video: {e}"

# Function to run the async code
async def get_video_summary(video_id: str):
    """Wrapper function to run async code."""
    return await summarize_video(video_id)

if __name__ == "__main__":
    # Example usage
    video_id = input("Enter YouTube video ID: ")
    summary = get_video_summary(video_id)
    print("\nSummary:")
    print(summary) 