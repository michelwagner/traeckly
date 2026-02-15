from traeckly_service import TraecklyReportInterface


class ConsoleReport(TraecklyReportInterface):
    def _pad_and_concat(self, str1: str, str2: str, str1_length: int) -> str:
        """Pad or truncate str1 to length and concatenate with str2."""
        return str1[:str1_length].ljust(str1_length) + str2


    def create_report(self, data: dict) -> None:
        from_time = data["from"].replace('T', ' ')
        to_time = data["to"].replace('T', ' ')
        print('Report from {} ... {}'.format(from_time, to_time))

        header = [('Task', 'Time spent')]
        table = header + data.get("tasks", [])
        # determine the longest task name to align columns
        max_task_len = min(40, 4 + max((len(t[0]) for t in table), default=0))  # 4 is for padding

        for task_name, total_time in table:
            print(self._pad_and_concat(task_name, total_time, max_task_len))

