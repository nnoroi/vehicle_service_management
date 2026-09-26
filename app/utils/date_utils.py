from datetime import datetime


def format_date_for_display(date_string):
    """Convert an ISO date into dd/mm/YYYY format"""

    if not date_string:
        return ""

    date = datetime.strptime(date_string, "%Y-%m-%d")
    return date.strftime("%d-%m-%Y")


def parse_uk_date(date_string):
    """Convert a UK date into ISO format for database storage"""

    if not date_string:
        return ""

    date = datetime.strptime(date_string, "%d-%m-%Y")
    return date.strftime("%Y-%m-%d")
