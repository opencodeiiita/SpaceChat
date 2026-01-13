#helpers.py
# Utility functions shared across the project.

import json
import os
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, '..', 'data', 'nasa_missions.json')

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.lower().split())

def _load_mission_data() -> list:
    if not os.path.exists(DATA_FILE_PATH):
        return []
        
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def get_mission_details(name: str) -> Dict[str, Any]:

    missions = _load_mission_data()
    if not missions:
        return {"error": "Mission data unavailable"}

    query = normalize_text(name)
    if not query:
        return {"error": "Empty query provided"}

    # Step 1: LLM-based semantic search (stub)
    
    # Importtant message : 
    # Replace this stub with actual LLM integration when we have that
    def llm_semantic_search(query, missions):
        # Simulate LLM output: find best match by fuzzy logic
        for mission in missions:
            m_name = normalize_text(mission.get("name", ""))
            if query in m_name or m_name in query:
                return mission
        return None

    llm_result = llm_semantic_search(query, missions)
    if llm_result:
        return _format_mission_output(llm_result)

    # Step 2: Keyword fallback (name, destination)
    for mission in missions:
        m_name = normalize_text(mission.get("name", ""))
        m_dest = normalize_text(mission.get("destination", ""))
        if query == m_name or query in m_name:
            return _format_mission_output(mission)
        if query == m_dest:
            return _format_mission_output(mission)

    # Step 3: Fallback to description search
    for mission in missions:
        desc = normalize_text(mission.get("description", ""))
        if query in desc:
            return _format_mission_output(mission)

    return {"error": "Mission not found"}


def _format_mission_output(mission: dict) -> dict:
    # Output schema enforcement
    required_keys = ["name", "description", "launch_date", "destination", "agency"]
    return {k: mission.get(k, "") for k in required_keys}

