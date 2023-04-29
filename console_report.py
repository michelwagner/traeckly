from traeckly_service import TraecklyReportInterface


class ConsoleReport(TraecklyReportInterface):
    def __init__(self):
        pass


    def __del__(self):
        pass


    def create_report(self, data):
        formating = '{}\t{}'
        print(formating.format('Task', 'Time spent'))
        for x in data:
            task_name = x[0]
            total_time = x[1]
            print(formating.format(task_name, total_time))


if __name__ == "__main__":
    print('console report')

    data = [('Break', '1:01'), ('Task-007', '0:00'), ('Task-123', '0:34'), ('Task-777', '0:00'), ('Task-778', '2:05')]
    report = ConsoleReport()
    report.create_report(data)
