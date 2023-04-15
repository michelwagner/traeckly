from traeckly_sqlite3 import TraecklySQLiteBackend
from traeckly_logging import TraecklyLoggingBackend

from traeckly_service import TraecklyService
import argparse


def parse_arguments(arguments = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_start = subparsers.add_parser('start')
    parser_start.add_argument('start_task')

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('create_task')

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
    service = TraecklyService(backend)

    if ("start_task" in args.keys()):
        service.start_task(args['start_task'])
    elif ("create_task" in args.keys()):
        print("create")
