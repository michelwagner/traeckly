from traeckly_sqlite3 import TraecklySQLiteBackend
from traeckly_logging import TraecklyLoggingBackend
from traeckly_service import TraecklyBackendBase
from console_report import ConsoleReport
import argparse
from datetime import datetime, timedelta


def create_backend():
    if (True):
        return TraecklySQLiteBackend()
    else:
        return TraecklyLoggingBackend();


def create_reporter():
    report = ConsoleReport()
    return report

    
def parse_arguments(arguments = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_start = subparsers.add_parser('start')
    parser_start.add_argument('task_name')

    parser_start = subparsers.add_parser('stop')

    parser_report = subparsers.add_parser('report')
    parser_report.add_argument('--out')
    parser_report.add_argument('timespan', nargs='+')

    args = parser.parse_args(arguments)
    return vars(args)


def _get_keyword_range(timespan_key: str) -> tuple[str, str] | None:
    now = datetime.now()
    
    if (timespan_key == 'day'):
        # get beginning of current day (00:00:00)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        result = (start_of_day.isoformat(timespec='seconds'), now.isoformat(timespec='seconds'))
    elif (timespan_key == 'week'):
        # get beginning of current week (Monday at 00:00:00)
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        result = (start_of_week.isoformat(timespec='seconds'), now.isoformat(timespec='seconds'))
    elif (timespan_key == 'month'):
        # get beginning of current month (1st day at 00:00:00)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        result = (start_of_month.isoformat(timespec='seconds'), now.isoformat(timespec='seconds'))
    else:
        result = None

    return result


def _get_days_range(days_text: str) -> tuple[str, str] | None:
    try:
        days = int(days_text)
        now = datetime.now()
        if (days > 0):
            start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            delta_in_days = timedelta(days = days - 1)
            from_time_iso = (start_of_today - delta_in_days).isoformat(timespec='seconds')
            to_time_iso = now.isoformat(timespec='seconds')
            result = (from_time_iso, to_time_iso)
    except:
        result = None

    return result


def _get_two_iso_range(from_text: str, to_text: str) -> tuple[str, str] | None:
    try:
        from_time_iso = datetime.fromisoformat(from_text).isoformat(timespec='seconds')
        to_time_iso = datetime.fromisoformat(to_text).isoformat(timespec='seconds')
        result = (from_time_iso, to_time_iso)
    except:
        result = None

    return result


def get_from_to_time_iso(timespan: list[str]) -> tuple[str, str]:
    """Return ISO-8601 start/end timestamps for a report timespan.

    Args:
        timespan: A list of one or two strings. If one element is provided, it
            can be an integer number of days (e.g. ["7"]) or a keyword
            ("day", "week", "month") for the current period. If two elements
            are provided, they are treated as ISO-8601 timestamps
            (e.g. ["2026-02-01T00:00:00", "2026-02-15T23:59:59"]).

    Returns:
        A tuple of (from_time_iso, to_time_iso). Empty strings are returned if
        parsing fails.
    """
    result = ('', '')

    if (len(timespan) == 1):
        timespan_0 = timespan[0].lower()

        keyword_range = _get_keyword_range(timespan_0)
        if (keyword_range is not None):
            result = keyword_range
        else:
            days_range = _get_days_range(timespan_0)
            if (days_range is not None):
                result = days_range

    elif (len(timespan) == 2):
        two_range = _get_two_iso_range(timespan[0], timespan[1])
        if (two_range is not None):
            result = two_range

    return result


if __name__ == "__main__":
    args = parse_arguments()
    backend = create_backend()

    if (args['command'] == "start"):        
        backend.start_task(args['task_name'])
    if (args['command'] == "stop"):
        backend.start_task(None)
    elif (args['command'] == "report"):
        (from_time, to_time) = get_from_to_time_iso(args['timespan'])
        task_data = backend.get_task_durations(from_time, to_time)
        report = create_reporter()
        report.create_report(task_data)
