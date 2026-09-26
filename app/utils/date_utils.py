from datetime import datetime


def format_date_for_display(date_string):
    """Convert an ISO date into dd/mm/YYYY format"""

    if not date_string:
        return ""

    date = datetime.strptime(date_string, "%Y-%m-%d")
    return date.strftime("%d-%m-%Y")
