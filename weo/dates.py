from datetime import datetime, date

from typing import List, Tuple, Iterator

__all__ = ['dates', '__all_dates__']

Date = Tuple[int, int]

def cur_year() -> int:
    return datetime.today().year

def cur_month() -> int:    
    return datetime.today().month

cy, cm = cur_year(), cur_month()

def in_range(t: Date) -> bool:
    return (2007, 10) <= t <= (cy, cm)

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

