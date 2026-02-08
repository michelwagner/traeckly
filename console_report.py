from traeckly_service import TraecklyReportInterface


class ConsoleReport(TraecklyReportInterface):
    def __init__(self):
        pass


    def __del__(self):
        pass


    def create_report(self, data):
        from_to_formatting = 'Report from {} to {}'
        print(from_to_formatting.format(data["from"], data["to"]))

        tasks = data.get("tasks", [])
        # determine the longest task name to align columns
        max_task_len = max((len(t[0]) for t in tasks), default=len('Task'))

        header_task = 'Task'
        header_time = 'Time spent'
        print(f"{header_task.ljust(max_task_len)}\t{header_time}")

        for task_name, total_time in tasks:
            print(f"{task_name.ljust(max_task_len)}\t{total_time}")


if __name__ == "__main__":
    print('console report')

    data = {'from': '2026-01-01', 'to': '2026-01-02', 'tasks': [('Break', '1:01'), ('Task-007', '0:00'), ('Task-123', '0:34'), ('Task-777', '0:00'), ('Task-778', '2:05')]}
    report = ConsoleReport()
    report.create_report(data)
