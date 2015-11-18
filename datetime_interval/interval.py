"""
Interval represents a duration of time at a specific point in time.
"""

from datetime import date, timedelta


class IntervalError(Exception):
    pass


class IntervalComparisonError(IntervalError):
    """
    Raised when comparing unequal but overlapping Intervals.
    """
    pass


class Interval(object):
    """
    An interval represents a duration of time and its location on the
    timeline. It can be any of the following:

    - start and end dates (or datetimes)
    - a start date (or datetime) and a timedelta
    - a timedelta and an end date (or datetime)

    Provides the following operators:
        for pairs of Intervals:
            is
            is not
            ==
            !=
            <
            <=
            >
            >=

        for a date and an Interval:
            in

        for an Interval and a timedelta:
            +
            -
    """

    # TODO: Add periodic operators:

    # Periodic: *
    #      Interval * int => (Bounded) PeriodicInterval
    #      Interval * forever => (Unbounded) PeriodicInterval
    #      Interval * _ => TypeError
    #      _ * Interval => TypeError
    #      PeriodicInterval * _ => TypeError
    #      _ * PeriodicInterval => TypeError

    # Indexing:
    #      PeriodicInterval[int] => Interval | ValueError
    #      PeriodicInterval[_] = > TypeError

    is_periodic = False

    start = None
    duration = None
    end = None

    def __init__(self, start=None, duration=None, end=None):
        """
        Construct an Interval object.
        """
        # Repair argument mishandling:
        if start and duration and not end:
            # There were just two arguments provided.
            if isinstance(start, timedelta) and isinstance(duration, date):
                # Was provided duration and end, so move them around.
                start, duration, end = None, start, duration

            if isinstance(start, date) and isinstance(duration, date):
                # Was provided start and end, so move them around.
                duration, end = end, duration

        # Type checking:
        assert isinstance(start, date) or not start
        assert isinstance(duration, timedelta) or not duration
        assert isinstance(end, date) or not end

        # Fill in the missing value:
        if duration and end and not start:
            start = end - duration
        if start and end and not duration:
            duration = end - start
        if start and duration and not end:
            end = start + duration
        assert start and duration and end

        # Assign the values:
        self.start = start
        self.duration = duration
        self.end = end

        self._invariants()

    @staticmethod
    def _timedelta_is_positive(tdelta):
        """
        Is the given timedelta positive?
        """
        return tdelta == abs(tdelta)

    def _invariants(self):
        """
        Assert invariants.
        """
        assert isinstance(self.start, date)
        assert isinstance(self.duration, timedelta)
        assert isinstance(self.end, date)
        assert self._timedelta_is_positive(self.duration)
        assert self.start <= self.end

    def __cmp__(self, other):
        """
        Provides comparison operators for two Intervals.

        Intervals are only comparable if they do not overlap. The two intervals
        must be strictly less than or greater than each other. Comparison of
        overlapping intervals will raise IntervalComparisonError.
        """
        # TODO: Handle periodic intervals.
        assert isinstance(other, Interval)
        equals = (
            self.start == other.start
            and self.duration == other.duration
            and self.end == other.end
            and self.is_periodic == other.is_periodic
        )
        if equals:
            return 0

        less_than = (
            self.start < other.start
            and self.end < other.end
        )
        if less_than:
            return -1

        greater_than = (
            self.start > other.start
            and self.end > other.end
        )
        if greater_than:
            return 1
        raise IntervalComparisonError

    def __contains__(self, item):
        """
        Checks if a date is contained within the Interval, e.g.:

        >>> datetime.now() in Interval(datetime.now(), timedelta(1))
        True
        """
        assert isinstance(item, date)
        return (
            self.start <= item
            and self.end >= item
        )

    def __add__(self, other):
        """
        Return a new Interval, moved ahead by other (a timedelta).
        """
        # TODO:
        # Interval + Interval => Interval | ValueError
        # Interval + _ => TypeError
        assert isinstance(other, timedelta)
        return Interval(
            self.start + other,
            self.duration
        )

    def __sub__(self, other):
        """
        Return a new Interval, moved back by other (a timedelta).
        """
        # TODO:
        # Interval - Interval => Interval | ValueError
        # Interval - _ => TypeError
        assert isinstance(other, timedelta)
        return Interval(
            self.start - other,
            self.duration
        )

    def __repr__(self):
        return 'Interval(start={self.start}, end={self.end}, duration={self.duration})'.format(self=self)

    def issuperset(self, other):
        """
        Test whether `other` is fully contained in this interval.
        """
        return self.start < other.start and self.end > other.end

    def issubset(self, other):
        """
        Test whether this interval is fully contained in the other interval.
        """
        return self.start > other.start and self.end < other.end

    def intersection(self, other):
        """
        Return a new Interval, defined by the intersection of this interval and the other interval.

        If the intervals are disjoint, raises IntervalError.
        """
        try:
            intervals_overlap = self.start in other or self.end in other
            assert intervals_overlap or self.issuperset(other) or self.issubset(other)
        except AssertionError:
            raise IntervalError('Intervals do not intersect')

        start = max(self.start, other.start)
        end = min(self.end, other.end)
        return Interval(start=start, end=end)
