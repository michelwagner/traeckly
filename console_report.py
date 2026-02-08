from traeckly_service import TraecklyReportInterface


class ConsoleReport(TraecklyReportInterface):
    def __init__(self):
        pass


    def __del__(self):
        pass


    def pad_and_concat(self, str1, str2, str1_length):
        """Pad or truncate str1 to length and concatenate with str2."""
        return str1[:str1_length].ljust(str1_length) + str2


    def create_report(self, data):
        from_to_formatting = 'Report from {} to {}'
        print(from_to_formatting.format(data["from"], data["to"]))

        header = [('Task', 'Time spent')]
        table = header + data.get("tasks", [])
        # determine the longest task name to align columns
        max_task_len = min(40, 4 + max((len(t[0]) for t in table), default=0))  # 4 is for padding

        for task_name, total_time in table:
            print(self.pad_and_concat(task_name, total_time, max_task_len))


if __name__ == "__main__":
    print('console report')

    data = {'from': '2026-01-01', 'to': '2026-01-02', 'tasks': [('Break', '1:01'), ('Task-007', '0:00'), ('Task-123', '0:34'), ('Task-777', '0:00'), ('Task-778', '2:05')]}
    report = ConsoleReport()
    report.create_report(data)
