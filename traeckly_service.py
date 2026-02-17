import re
from typing import Optional


class TraecklyBackendInterface:
    """Interface for backend implementations that manage task tracking storage."""
    
    def start_task(self, id: Optional[str]) -> None:
        """Start tracking a new task or stop tracking if id is None.
        
        Args:
            id: Task identifier string, or None to stop tracking.
        """
        raise NotImplementedError()
    
    def get_task_durations(self, from_isotime: str, to_isotime: str) -> dict:
        """Get task durations for a specified time range.
        
        Args:
            from_isotime: Start time in ISO format.
            to_isotime: End time in ISO format.
            
        Returns:
            Dictionary with 'from', 'to', and 'tasks' (list of tuples).
        """
        raise NotImplementedError()


class TraecklyBackendBase(TraecklyBackendInterface):
    """Base class for backend implementations with common utility methods."""

    @staticmethod
    def _normalize_task_name(item: str) -> str:
        """Replace non-printable characters (including whitespace) with '_' ."""
        return re.sub(r'\W', '_', item) if item else item
    
    def _format_time_difference(self, delta_time_seconds: float) -> str:
        """Format time difference in seconds as hours:minutes string.
        
        Args:
            delta_time_seconds: Time difference in seconds.
            
        Returns:
            Formatted string in 'H:MM' format.
        """
        hours = int(delta_time_seconds) // 3600
        minutes = round((delta_time_seconds - (hours * 3600.0)) / 60.0)
        return f"{hours}:{minutes:02d}"



class TraecklyReportInterface:
    """Interface for report generators that display task tracking data."""
    
    def create_report(self, data: dict) -> None:
        """Generate and display a report from task duration data.
        
        Args:
            data: Dictionary containing 'from', 'to', and 'tasks' keys.
        """
        raise NotImplementedError()
