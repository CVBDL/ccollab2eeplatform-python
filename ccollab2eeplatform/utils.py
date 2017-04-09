"""Custom utils."""

from datetime import date
from itertools import groupby as groupby_


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
    return from_isoformat(date_str).isoformat()


def from_isoformat(date_str):
    """Create date from iso string."""
    message = 'Date should be in ISO 8601 format: "YYYY-MM-DD"'
    if not isinstance(date_str, str):
        raise Exception(message)
    try:
        parts = [int(part) for part in date_str.split('-')]
        return date(parts[0], parts[1], parts[2])
    except:
        raise Exception(message)


def month_range(start, stop):
    """Return a year month range.

    Args:
        start (str): Start year month in format '2016-01'
        stop (str): Stop year month in format '2017-01'
    Returns:
        A list of year month string.
    Examples:
        >>> month_range('2016-11', '2017-01')
        ['2016-11', '2016-12', '2017-01']
        >>> month_range('2017-01', '2016-11')
        ['2017-01', '2016-12', '2016-11']
    """
    start_date = from_isoformat('{0}-01'.format(start))
    stop_date = from_isoformat('{0}-01'.format(stop))

    if start_date > stop_date:
        start_date, stop_date = stop_date, start_date
        reverse = True
    else:
        reverse = False

    result = []
    while start_date <= stop_date:
        result.append(start_date.isoformat()[0:7])
        year = start_date.year
        month = start_date.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        start_date = date(year, month, 1)

    return reverse and sorted(result, reverse=reverse) or result


def groupby(iterable, key=None, reverse=False):
    """Wrapper of itertools.groupby function.

    It make use of built-in itertools.groupby function.
    In addition to sort the iterable with the same key as groupby.
    Ref: <https://docs.python.org/3/library/itertools.html#itertools.groupby>
    """
    if key is None:
        key = lambda x: x
    return groupby_(sorted(iterable, key=key, reverse=reverse), key)
