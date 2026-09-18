"""
Simple keyword-based expense category predictor.

This module intentionally avoids machine learning so that it stays easy
to read and explain in a college mini-project report. It simply scans the
expense description for known keywords (case-insensitive) and returns the
matching category. If nothing matches, it falls back to "Other".
"""

CATEGORY_KEYWORDS = {
    "Food": [
        "food", "pizza", "burger", "restaurant", "coffee", "tea", "lunch",
        "dinner", "breakfast", "snack", "swiggy", "zomato", "canteen",
        "juice", "bakery", "grocery", "groceries",
    ],
    "Travel": [
        "uber", "ola", "bus", "train", "taxi", "fuel", "petrol", "diesel",
        "travel", "flight", "cab", "metro", "auto", "parking", "toll",
    ],
    "Shopping": [
        "shirt", "dress", "shoes", "clothes", "shopping", "amazon",
        "flipkart", "myntra", "mall", "jeans", "bag", "watch",
    ],
    "Bills": [
        "electricity", "water", "internet", "mobile", "bill", "recharge",
        "wifi", "broadband", "rent", "gas", "dth",
    ],
    "Entertainment": [
        "movie", "cinema", "game", "netflix", "music", "concert", "spotify",
        "prime video", "hotstar", "pvr", "bookmyshow", "outing",
    ],
    "Health": [
        "doctor", "medicine", "hospital", "medical", "pharmacy", "clinic",
        "health", "gym", "dentist", "checkup",
    ],
    "Education": [
        "book", "college", "course", "exam", "education", "tuition",
        "fees", "stationery", "udemy", "library", "workshop",
    ],
}


def predict_category(description: str) -> str:
    """Predict an expense category from its description text.

    Args:
        description: Free-text description of the expense.

    Returns:
        The predicted category name, or "Other" if no keyword matches.
    """
    if not description:
        return "Other"

    text = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Other"
