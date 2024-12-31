from fastapi import FastAPI, Query
from typing import List, Optional
import pandas as pd
import os

# Load drills data
DATA_PATH = os.path.join("data", "drills.csv")
drills_data = pd.read_csv(DATA_PATH)

# Initialize FastAPI app
app = FastAPI(title="Rakket AI", description="Tennis Drill Recommendation System", version="0.1")

# Helper function to filter drills
def filter_drills(focus_area: Optional[str] = None, difficulty: Optional[str] = None, num_players: Optional[int] = None):
    filtered_data = drills_data
    if focus_area:
        filtered_data = filtered_data[filtered_data["Focus Area"].str.contains(focus_area, case=False, na=False)]
    if difficulty:
        filtered_data = filtered_data[filtered_data["Difficulty"].str.contains(difficulty, case=False, na=False)]
    if num_players:
        filtered_data = filtered_data[filtered_data["Number of Players"].astype(str).str.contains(str(num_players), na=False)]
    return filtered_data[["Drill Name", "Focus Area", "Difficulty", "Description"]].to_dict(orient="records")

# API route for drill recommendations
@app.get("/recommend-drills", response_model=List[dict])
def recommend_drills(
    focus_area: Optional[str] = Query(None, description="Focus area of the drill (e.g., Consistency, Accuracy)"),
    difficulty: Optional[str] = Query(None, description="Difficulty level (e.g., Beginner, Intermediate, Advanced)"),
    num_players: Optional[int] = Query(None, description="Number of players (e.g., 1, 2, 4)")
):
    """
    Recommend tennis drills based on user preferences.
    """
    return filter_drills(focus_area, difficulty, num_players)