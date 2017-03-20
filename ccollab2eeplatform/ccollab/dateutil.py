from datetime import date


def to_isoformat(date_str):
    message = 'Error occurred parsing date to ISO format.'

    if not isinstance(date_str, str):
        raise Exception(message)

    try:
        parts = [ int(part) for part in date_str.split('-') ]
        return date(parts[0], parts[1], parts[2]).isoformat()
    except:
        raise Exception(message)
