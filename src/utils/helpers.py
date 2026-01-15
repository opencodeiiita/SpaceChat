def get_mission_details(name: str) -> dict:
    """
    Fetch mission details by mission name.
    """

    if not name or not name.strip():
        return {"error": "Mission name cannot be empty."}

    data_path = os.path.join("data", "nasa_missions.json")

    try:
        with open(data_path, "r", encoding="utf-8") as file:
            missions = json.load(file)
    except FileNotFoundError:
        return {"error": "Mission data file not found."}
    except json.JSONDecodeError:
        return {"error": "Mission data file is corrupted."}

    search_name = name.strip().lower()

    # 1. Exact match
    for mission in missions:
        if mission.get("name", "").lower() == search_name:
            return mission

    # 2. Partial / keyword match
    for mission in missions:
        if search_name in mission.get("name", "").lower():
            return mission

    return {
        "error": f"Mission '{name}' not found."
    }
