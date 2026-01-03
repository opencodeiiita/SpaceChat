#helpers.py
# Utility functions shared across the project.


def normalize_text(arg :str) -> str:
    # Ig argument is None empty string is returned
    if arg == None:
        return ""
    return " ".join(arg.lower().split())

