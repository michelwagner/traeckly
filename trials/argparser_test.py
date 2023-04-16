import argparse


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
    print(args)
    print(vars(args))


if __name__ == "__main__":
    args = parse_arguments()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('command', choices=['start', 'stop', 'report'], nargs=1)
    # parser.add_argument('options', nargs='*')
    # args = parser.parse_args()
    
    # print(args)