from datetime import datetime, date

from typing import List, Tuple, Iterator

__all__ = ['dates', '__all_dates__',  'parse_and_validate']

Date = Tuple[int, int]

def cur_year() -> int:
    return datetime.today().year

def cur_month() -> int:    
    return datetime.today().month

CURRENT_YEAR, CURRENT_MONTH = cur_year(), cur_month()

def in_range(t: Date) -> bool:
    return (2007, 10) <= t <= (CURRENT_YEAR, CURRENT_MONTH)

def adjust(t: Date) -> Date:
    exceptions = {(2011, 10): (2011, 9)}
    return exceptions.get(t, t)

def raw_tuples() -> List[Date]:
    return [(y,m) for y in range(2007,  cur_year()+1) for m in [4, 10]]

def allowed_tuples() -> Iterator[Date]:
    xs = filter(in_range, raw_tuples())
    return map(adjust, xs)

def to_string(t: Date)-> str:
    return date(*t, 1).strftime("%Y-%b")

def as_dates(xs: Iterator[Date])->List[str]:
    return list(map(to_string, xs))

def all_dates()->List[str]:   
    return as_dates(allowed_tuples())
    
def dates(year: int)->List[str]:
    def this_year(t):
        return t[0] == year
    xs = filter(this_year, allowed_tuples())
    return as_dates(xs)


class WEO_DateError(ValueError):
    pass


def validate(year: int, month: int):
    text = to_string((year, month))
    exceptions = [(2011, 9)]
    if (year, month) < (2007, 10):
        raise WEO_DateError(f"Cannot work with date earlier than 2007-Oct, got {text}")
    if (year, month) > (CURRENT_YEAR, CURRENT_MONTH):
        raise WEO_DateError(f"The date is in the future, got {text}")
    if month not in [4, 10] and (year, month) not in exceptions:
        raise WEO_DateError(f"Usual accepted months are Apr and Oct, got {text}")


def parse_date_string(s: str) -> Date:
    for fmt in "%Y-%b", "%Y-%m", "%Y-%B":
        try:
            dt = datetime.strptime(s, fmt)
            return dt.year, dt.month
        except ValueError:
            pass
    raise ValueError(s)

def parse_and_validate(s: str) -> Date:
    year, month = parse_date_string(s)
    validate(year, month)
    return year, month