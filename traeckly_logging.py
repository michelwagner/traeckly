from traeckly_service import TraecklyBackendBase
from typing import Optional
import logging
import time


class TraecklyLoggingBackend(TraecklyBackendBase):
    """Backend implementation that logs task tracking events to a file.
    
    This backend writes task start/stop events and durations to a log file
    but does not support retrieving historical task duration data.
    """
    
    def __init__(self, filename):
        """Initialize the logging backend with default configuration."""
        self._start_time = 0
        self._active_task = None
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S',
            filename=filename,
            encoding='utf-8',
            level=logging.DEBUG
        )

    def start_task(self, id: Optional[str]) -> None:
        """Start tracking a new task or stop tracking if id is None.
        
        Args:
            id: Task identifier string, or None to stop tracking.
        """
        if self._active_task is not None:
            self._show_delta_time()

        self._start_time = time.time()
        self._active_task = id
        self._log(f"{id} started")

    def get_task_durations_sum(self, from_isotime: str, to_isotime: str) -> dict:
        """Get task durations - not supported by logging backend.
        
        Args:
            from_isotime: Start time in ISO format (ignored).
            to_isotime: End time in ISO format (ignored).
            
        Returns:
            Dictionary with empty tasks list.
        """
        return {"from": from_isotime, "to": to_isotime, "tasks": []}

    def _show_delta_time(self) -> None:
        """Calculate and log the duration of the currently active task."""
        delta_time = time.time() - self._start_time
        s = self._format_time_difference(delta_time)
        self._log(f"{self._active_task} duration {s}")

    def _log(self, message: str) -> None:
        """Write a message to the log file.
        
        Args:
            message: The message to log.
        """
        logging.info(message)
