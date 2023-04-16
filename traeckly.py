from traeckly_sqlite3 import TraecklySQLiteBackend
from traeckly_logging import TraecklyLoggingBackend
from console_report import ConsoleReport
import argparse
from datetime import datetime


def create_backend():
    if (True):
        return TraecklySQLiteBackend()
    else:
        return TraecklyLoggingBackend();


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


def get_from_to_isotimes(timespan):
    try:
        t1_iso = datetime.fromisoformat(timespan[0]).isoformat(timespec='seconds')
        t2_iso = datetime.fromisoformat(timespan[1]).isoformat(timespec='seconds')
    except:
        t1_iso = ''
        t2_iso = ''
        
    return (t1_iso, t2_iso)


if __name__ == "__main__":
    args = parse_arguments()
    backend = create_backend()

    if (args['command'] == "start"):
        backend.start_task(args['task_name'])
    if (args['command'] == "stop"):
        backend.start_task(None)
    elif (args['command'] == "report"):
        report = ConsoleReport()
        from_to_times = get_from_to_isotimes(args['timespan'])
        task_data = backend.get_task_durations(from_to_times[0], from_to_times[1])
        report.create_report(task_data)
