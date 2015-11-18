from datetime import datetime, timedelta

from datetime_interval import Interval

from datetime_interval.interval import IntervalError


def pairs(lst):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first


def test_last_next(last24, next24):
    assert last24 is not next24
    assert next24 is not last24
    assert last24 != next24
    assert last24 < next24
    assert next24 > last24
    assert last24 <= next24
    assert next24 >= last24


now = datetime.now()
yesterday = now - timedelta(1)
tomorrow = now + timedelta(1)

last24s = [
    Interval(yesterday, now),
    Interval(yesterday, timedelta(1)),
    Interval(timedelta(1), now)
]

next24s = [
    Interval(now, tomorrow),
    Interval(now, timedelta(1)),
    Interval(timedelta(1), tomorrow)
]

for last24, last24_ in pairs(last24s):
    assert last24 is last24
    assert last24 is not last24_
    assert last24 == last24
    assert last24 == last24_
    assert last24 <= last24
    assert last24 <= last24_
    assert last24 >= last24
    assert last24 >= last24_

for next24, next24_ in pairs(next24s):
    assert next24 is next24
    assert next24 is not next24_
    assert next24 == next24
    assert next24 == next24_
    assert next24 <= next24
    assert next24 <= next24_
    assert next24 >= next24
    assert next24 >= next24_

for last24 in last24s:
    for next24 in next24s:
        test_last_next(last24, next24)

for last24 in last24s:
    assert yesterday in last24
    assert now in last24
    assert tomorrow not in last24
    next24 = last24 + timedelta(1)
    test_last_next(last24, next24)

for next24 in next24s:
    assert yesterday not in next24
    assert now in next24
    assert tomorrow in next24
    last24 = next24 - timedelta(1)
    test_last_next(last24, next24)


jan_start = datetime(2015, 1, 1)
jan_mid = datetime(2015, 1, 15)
jan_end = datetime(2015, 1, 31)
jan_all = Interval(start=jan_start, end=jan_end)
jan_half = Interval(start=jan_start, end=jan_mid)

mar_start = datetime(2015, 3, 1)
mar_end = datetime(2015, 3, 31)
mar_all = Interval(start=mar_start, end=mar_end)

jan_feb = Interval(start=datetime(2015, 1, 25), end=datetime(2015, 2, 10))

assert jan_all.intersection(jan_half) == jan_half.intersection(jan_all)
assert jan_feb.intersection(jan_all) == jan_all.intersection(jan_feb)
assert jan_all.intersection(jan_half) == Interval(start=jan_start, end=jan_mid)
assert jan_feb.intersection(jan_all) == Interval(start=jan_feb.start, end=jan_all.end)
try:
    jan_all.intersection(mar_all)
    raise AssertionError('Expected IntervalError not raised.')
except IntervalError:
    pass

try:
    mar_all.intersection(jan_all)
    raise AssertionError('Expected IntervalError not raised.')
except IntervalError:
    pass

print('All tests passed.')
