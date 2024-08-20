from dateutil import parser

def date_format(date_str: str) -> str:
    """
    Converts a date string to the format '%Y-%m-%d'.

    The function attempts to parse the input date string using several common date formats.
    If successful, it returns the date in the '%Y-%m-%d' format. If none of the formats match,
    it raises a ValueError.

    Parameters:
        date_str (str): The date string to be formatted.

    Returns:
        str: The date in '%Y-%m-%d' format.

    Raises:
        ValueError: If the date string does not match any of the supported formats.
    """
    try:
        date_obj = parser.parse(date_str)
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Date format for '{date_str}' is not supported")
