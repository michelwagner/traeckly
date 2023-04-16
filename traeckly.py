from traeckly_sqlite3 import TraecklySQLiteBackend
from traeckly_logging import TraecklyLoggingBackend

# from traeckly_service import TraecklyService
import argparse


def parse_arguments(arguments = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_start = subparsers.add_parser('start')
    parser_start.add_argument('start_task')

    parser_create = subparsers.add_parser('report')
    parser_create.add_argument('-w', '--weekly', action='store_true')

    args = parser.parse_args(arguments)
    return vars(args)


def create_backend():
    if (True):
        return TraecklySQLiteBackend()
    else:
        return TraecklyLoggingBackend();


if __name__ == "__main__":
    args = parse_arguments()
    backend = create_backend()
    # service = TraecklyService(backend)

    if ("start_task" in args.keys()):
        backend.start_task(args['start_task'])
    elif ("report" in args.keys()):
        backend.report('2023-04-09 11:45:21', '2023-04-16 11:45:21')
