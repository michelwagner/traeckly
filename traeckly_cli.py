import argparse


def parse_arguments(arguments = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('create_task')

    parser_start = subparsers.add_parser('start')
    parser_start.add_argument('start_task')

    args = parser.parse_args(arguments)
    return vars(args)


if __name__ == "__main__":
    print("Traeckly cli")

    args = parse_arguments()

    if ("create_task" in args.keys()):
        print("create")
    elif ("start_task" in args.keys()):
        print("start")
