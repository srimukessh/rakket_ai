from fastapi import FastAPI, Query
from typing import List, Optional
import pandas as pd
from pydantic_ai import Agent, Tool, RunContext
from dotenv import load_dotenv
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware



# Activate the virtual environment: source venv/bin/activate
# To run : uvicorn main:app --reload

load_dotenv()
# Load drills data
DATA_PATH = "data/drills.csv"
drills_data = pd.read_csv(DATA_PATH)

# Initialize FastAPI app
app = FastAPI(title="Rakket AI", description="Tennis Drill Recommendation System", version="0.1")

# Add CORS middleware right after app initialization
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rakket.io",          # Production
        "https://www.rakket.io",      # Production with www
        "http://localhost:3000",      # Local frontend development
        "http://127.0.0.1:8000",     # Local FastAPI development
        "http://localhost:8000"       # Alternative local FastAPI address
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to filter drills based on user inputs
def filter_drills(focus_area: Optional[str] = None, difficulty: Optional[str] = None, num_players: Optional[int] = None, shot_type: Optional[str] = None):
    filtered_data = drills_data
    if focus_area:
        filtered_data = filtered_data[filtered_data["Focus Area"].str.contains(focus_area, case=False, na=False)]
    if difficulty:
        filtered_data = filtered_data[filtered_data["Difficulty"].str.contains(difficulty, case=False, na=False)]
    if num_players:
        filtered_data = filtered_data[filtered_data["Number of Players"].astype(str).str.contains(str(num_players), na=False)]
    if shot_type:
        filtered_data = filtered_data[filtered_data["Shot/Type"].str.contains(shot_type, case=False, na=False)]
    return filtered_data[["Drill Name", "Focus Area", "Difficulty", "Shot/Type", "Description"]].to_dict(orient="records")

# GET: API route for drill recommendations based on query parameters
@app.get("/recommend-drills", response_model=List[dict])
def recommend_drills(
    focus_area: Optional[str] = Query(None, description="Focus area of the drill (e.g., Consistency, Accuracy)"),
    difficulty: Optional[str] = Query(None, description="Difficulty level (e.g., Beginner, Intermediate, Advanced)"),
    num_players: Optional[int] = Query(None, description="Number of players (e.g., 1, 2, 4)"),
    shot_type: Optional[str] = Query(None, description="Type of shot or drill focus (e.g., Volley, Serve, Groundstrokes)")
):
    """
    Recommend tennis drills based on focus area, difficulty level, number of players, and shot type.
    """
    return filter_drills(focus_area, difficulty, num_players, shot_type)

# Define the tool function with stricter type handling
def recommend_drills_tool(
    ctx: RunContext,
    focus_area: str = None,  # Default to an empty string
    difficulty: str = None,  # Default to an empty string
    num_players: int = None,  # Default to 0
    shot_type: str = None     # Default to an empty string
) -> list:
    """
    Tool function to recommend drills based on user input.
    Handles optional parameters explicitly by providing defaults.
    """
    # Use defaults if values are missing
    focus_area = focus_area or "Consistency"
    difficulty = difficulty or ""
    num_players = num_players or 2
    shot_type = shot_type or ""

    # Implement filtering logic
    return filter_drills(focus_area, difficulty, num_players, shot_type)

# Wrap the tool function
recommend_drills_tool_wrapper = Tool(
    recommend_drills_tool,
    description="Recommend tennis drills based on user inputs like focus area, difficulty, number of players, and shot type."
)

# Create an AI agent
agent = Agent(
    model='gemini-1.5-flash',
    system_prompt=(
        "You are a tennis coach helping users find the best drills. "
        "If the user does not provide all or any inputs, use the default values: "
        "Focus Area = 'Consistency', Difficulty = 'Intermediate', Number of Players = 2, Shot Type = ''."
    ),
    tools=[recommend_drills_tool_wrapper]
)

# POST: AI-powered natural language endpoint
@app.post("/ai-recommend-drills")
async def ai_recommend_drills(message: str):
    """
    Recommend tennis drills based on a natural language query using Pydantic AI Agent.
    """
    # Process the message with the AI agent
    result = await agent.run(message)
    return {"response": result.data}