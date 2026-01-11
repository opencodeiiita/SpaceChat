#research_tool.py
#handles research, external data and information gathering

import json
import os
from typing import List, Dict, Optional


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data', 'nasa_missions.json')

def load_missions() -> List[Dict]:
    """Helper to load mission data from JSON file."""
    try:
        if not os.path.exists(DATA_FILE_PATH):
            print(f"Warning: {DATA_FILE_PATH} not found.")
            return []
            
        with open(DATA_FILE_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mission data: {e}")
        return []

def _llm_extract_mission_name(query: str, mission_names: List[str]) -> Optional[str]:
    """
    Simulates the LLM-based semantic interpretation.
    
    TODO: In the future, import your 'llm_agent' here to make a real call 
    instead of this heuristic check.
    """
    query_lower = query.lower()
    
 
    if "first" in query_lower and "moon" in query_lower and "Apollo 11" in mission_names:
        return "Apollo 11"
        
    return None 

def get_mission_details(name: str) -> dict:
    """
    Searches for mission details using an LLM-first approach with keyword fallback.
    
    Args:
        name (str): The search query or mission name.
        
    Returns:
        dict: The mission details or an error dictionary.
    """
    missions = load_missions()
    mission_names = [m.get("name") for m in missions]
    
    found_mission = None

    suggested_name = _llm_extract_mission_name(name, mission_names)
    
    if suggested_name:
        for mission in missions:
            if mission.get("name") == suggested_name:
                found_mission = mission
                break

    if not found_mission:
        query_normalized = name.lower().strip()
        for mission in missions:
            m_name = mission.get("name", "").lower()
            if query_normalized in m_name or m_name in query_normalized:
                found_mission = mission
                break

    if found_mission:
        return {
            "name": found_mission.get("name", "Unknown"),
            "description": found_mission.get("description", "No description available."),
            "launch_date": found_mission.get("launch_date", "Unknown"),
            "destination": found_mission.get("destination", "Unknown"),
            "agency": found_mission.get("agency", "NASA")
        }
    else:
        return {
            "error": "Mission not found or data unavailable"
        }

if __name__ == "__main__":
    print(get_mission_details("Apollo 11"))
