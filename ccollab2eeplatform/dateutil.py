from datetime import date


def to_isoformat(date_str):
    """Convert an ISO 8601 like date string to standard ISO 8601 format.

    Args:
        date_str (str): An ISO 8601 like date string.
    Returns:
        str: A standard ISO 8601 date string.
    Examples:
        >>> to_isoformat('2017-1-1')
        2017-01-01
    """
    message = 'Error occurred parsing date to ISO format.'

    if not isinstance(date_str, str):
        raise Exception(message)

    try:
        parts = [ int(part) for part in date_str.split('-') ]
        return date(parts[0], parts[1], parts[2]).isoformat()
    except:
        raise Exception(message)
