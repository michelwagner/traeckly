from traeckly_service import TraecklyReportInterface


class ConsoleReport(TraecklyReportInterface):
    def __init__(self):
        pass


    def __del__(self):
        pass


    def create_report(self, data):
        task_duration_formatting = '{}\t{}'
        from_to_formatting = 'Report from {} to {}'
        print(from_to_formatting.format(data["from"], data["to"]))
        print(task_duration_formatting.format('Task', 'Time spent'))
        for x in data["tasks"]:
            task_name = x[0]
            total_time = x[1]
            print(task_duration_formatting.format(task_name, total_time))

if __name__ == "__main__":
    print('console report')

    data = {'from': '2026-01-01', 'to': '2026-01-02', 'tasks': [('Break', '1:01'), ('Task-007', '0:00'), ('Task-123', '0:34'), ('Task-777', '0:00'), ('Task-778', '2:05')]}
    report = ConsoleReport()
    report.create_report(data)
