def normalize_text(text):
    """
    Normalize input text for consistent processing.

    Steps:
    1. Handle None input safely.
    2. Convert text to lowercase.
    3. Remove leading and trailing whitespace.
    4. Replace multiple internal spaces, tabs, or newlines with a single space.

    Args:
        text (str): Input text to normalize.

    Returns:
        str: Cleaned and normalized text.
    """

    # Handle None input safely
    if text is None:
        return ""

    # Convert to string in case non-string input is passed
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Replace tabs and newlines with spaces
    text = text.replace("\n", " ").replace("\t", " ")

    # Remove leading/trailing spaces and normalize internal spacing
    text = " ".join(text.split())

    return text