#helpers.py
# Utility functions shared across the project.
#helpers.py
# Utility functions shared across the project.
import os
import json
import instructor
from groq import Groq
from pydantic import BaseModel
from typing import Optional


class MissionInterpretation(BaseModel):
    mission_name: Optional[str]
    mission_query: bool


# Path to the nasa_missions.json file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "nasa_missions.json")


# Loads missions data from the JSON file
def load_missions(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


# Using the OpenAI LLM 
def llm_extract(query: str) -> Optional[str]:
    try:
        client = instructor.from_groq(Groq(),mode=instructor.Mode.JSON)
        result = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_model=MissionInterpretation,
            messages=[
                {
                    "role": "system",
                    "content": "Extract the space mission name if the query refers to one.",
                },
                {"role": "user", "content": query},
            ],
        )
        return result.mission_name if result.mission_query else None
    except Exception:
        return None


def get_mission_details(name: str) -> dict:
    missions = load_missions(DATA_FILE_PATH)
    if not missions:
        return {"error": "error specs"}

    # LLM-first
    mission_name = llm_extract(name)
    if mission_name:
        for m in missions:
            if m.get("name", "").lower() == mission_name.lower():
                return {
                    "name": m.get("name"),
                    "description": m.get("description"),
                    "launch_date": m.get("launch_date"),
                    "destination": m.get("destination"),
                    "agency": m.get("agency", "NASA"),
                }

    # Keyword fallback
    query = name.lower()
    for m in missions:
        if m.get("name", "").lower() in query:
            return {
                "name": m.get("name"),
                "description": m.get("description"),
                "launch_date": m.get("launch_date"),
                "destination": m.get("destination"),
                "agency": m.get("agency", "NASA"),
            }

    return {"error": "error specs"}


def normalize_text(arg :str) -> str:
    # Ig argument is None empty string is returned
    if arg == None:
        return ""
    return " ".join(arg.lower().split())

# Testing

if __name__ == "__main__":
    test_queries = [
        "Tell me about the Apollo 11 mission.",
        "What was the launch date of Voyager 1?",
        "Give me details on the Mars Rover mission.",
        "Tell me about the James Webb Space Telescope.",
    ]

    for query in test_queries:
        details = get_mission_details(query)
        print(f"Query: {query}\nDetails: {details}\n")
