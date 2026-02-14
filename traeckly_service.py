import logging
from typing import Optional


class TraecklyBackendInterface:
    """Interface for backend implementations that manage task tracking storage."""
    
    def start_task(self, id: Optional[str]) -> None:
        """Start tracking a new task or stop tracking if id is None.
        
        Args:
            id: Task identifier string, or None to stop tracking.
        """
        pass
    
    def get_task_durations(self, from_isotime: str, to_isotime: str) -> dict:
        """Get task durations for a specified time range.
        
        Args:
            from_isotime: Start time in ISO format.
            to_isotime: End time in ISO format.
            
        Returns:
            Dictionary with 'from', 'to', and 'tasks' (list of tuples).
        """
        pass



class TraecklyReportInterface:
    """Interface for report generators that display task tracking data."""
    
    def create_report(self, data: dict) -> None:
        """Generate and display a report from task duration data.
        
        Args:
            data: Dictionary containing 'from', 'to', and 'tasks' keys.
        """
        pass
