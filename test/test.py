import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.helpers import get_mission_details

# existent mission
result_found = get_mission_details("Apollo 11")
print(json.dumps(result_found, indent=2, ensure_ascii=False))

# non-existent mission
result_not_found = get_mission_details("\nUnknown Mission")
print(json.dumps(result_not_found, indent=2, ensure_ascii=False))