from typing import List, Tuple

from traeckly_service import AbstractTraecklyReport


class ConsoleReport(AbstractTraecklyReport):
    @staticmethod
    def _render_table(rows: List[Tuple[str, str]], max_task_len: int = 40) -> List[str]:
        task_width = min(max_task_len, max((len(row[0]) for row in rows), default=0))
        time_width = max((len(row[1]) for row in rows), default=0)

        def border() -> str:
            return "+-" + "-" * task_width + "-+-" + "-" * time_width + "-+"

        def row_line(task: str, time_spent: str) -> str:
            task_cell = task[:task_width].ljust(task_width)
            time_cell = time_spent.rjust(time_width)
            return "| " + task_cell + " | " + time_cell + " |"

        lines = [border(), row_line(rows[0][0], rows[0][1]), border()]
        for task_name, total_time in rows[1:]:
            lines.append(row_line(task_name, total_time))
        lines.append(border())
        return lines


    def create_report(self, data: dict) -> None:
        from_time = data["from"].replace('T', ' ')
        to_time = data["to"].replace('T', ' ')
        print(f"Report from {from_time} ... {to_time}")

        header = [('Task', 'Time h:mm')]
        rows = header + [(task, str(total_time)) for task, total_time in data.get("tasks", [])]

        for line in self._render_table(rows):
            print(line)

