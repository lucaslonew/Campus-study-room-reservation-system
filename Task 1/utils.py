"""
utils.py
========
This module contains utility functions, validation helpers, and static methods
for the Campus Multi-Room Reservation System. It demonstrates OOP concepts
including Static Methods, Class Methods, and pure utility functions.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, List


# =============================================================================
# CLASS: ValidationUtils
# =============================================================================
# A utility class containing static methods for input validation.
# This class doesn't need to be instantiated - all methods are static.
# =============================================================================
class ValidationUtils:
    """
    Utility class for input validation.
    All methods are static - no instance creation needed.
    """
    
    # ==========================================================================
    # STATIC METHODS: Input validation without instance state
    # ==========================================================================
    
    @staticmethod
    def validate_student_id(student_id: str) -> Tuple[bool, str]:
        """
        STATIC METHOD:
        =============
        Validate that a student ID is exactly 8 digits.
        Returns a tuple of (is_valid, error_message).
        
        Parameters:
            student_id: The student ID string to validate
            
        Returns:
            Tuple (bool, str) - (is_valid, error_message_or_empty)
        """
        # Check if empty
        if not student_id:
            return (False, "Student ID cannot be empty")
        
        # Check length
        if len(student_id) != 8:
            return (False, "Student ID must be exactly 8 digits")
        
        # Check if all digits
        if not student_id.isdigit():
            return (False, "Student ID must contain only numbers (0-9)")
        
        # All checks passed
        return (True, "")
    
    @staticmethod
    def validate_date_time(date_str: str, time_str: str) -> Tuple[bool, str, Optional[datetime]]:
        """
        STATIC METHOD:
        =============
        Validate and parse date and time strings.
        
        Parameters:
            date_str: Date string in format "YYYY-MM-DD"
            time_str: Time string in format "HH:MM"
            
        Returns:
            Tuple (is_valid, error_message, datetime_object_or_None)
        """
        # Combine date and time
        datetime_str = f"{date_str} {time_str}"
        
        try:
            # Parse the combined string
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # Check if the datetime is in the future
            if dt < datetime.now():
                return (False, "Cannot make reservations in the past", None)
            
            return (True, "", dt)
        except ValueError:
            return (False, "Invalid date/time format. Use YYYY-MM-DD and HH:MM", None)
    
    @staticmethod
    def validate_datetime_range(start_str: str, end_str: str) -> Tuple[bool, str, Optional[datetime], Optional[datetime]]:
        """
        STATIC METHOD:
        =============
        Validate a datetime range (start and end).
        Format expected: "YYYY-MM-DD HH:MM" for both inputs.
        
        Parameters:
            start_str: Start datetime string
            end_str: End datetime string
            
        Returns:
            Tuple (is_valid, error_message, start_datetime, end_datetime)
        """
        # Parse start time
        try:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return (False, "Invalid start time format. Use YYYY-MM-DD HH:MM", None, None)
        
        # Parse end time
        try:
            end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return (False, "Invalid end time format. Use YYYY-MM-DD HH:MM", None, None)
        
        # Check if start is in the future
        if start_dt < datetime.now():
            return (False, "Start time must be in the future", None, None)
        
        # Check if end is after start
        if end_dt <= start_dt:
            return (False, "End time must be after start time", None, None)
        
        # Check if duration is reasonable (at least 15 minutes, max 4 hours)
        duration = end_dt - start_dt
        duration_minutes = duration.total_seconds() / 60
        
        if duration_minutes < 15:
            return (False, "Reservation must be at least 15 minutes", None, None)
        
        if duration_minutes > 240:  # 4 hours
            return (False, "Reservation cannot exceed 4 hours", None, None)
        
        return (True, "", start_dt, end_dt)
    
    @staticmethod
    def validate_group_size(size_str: str, max_capacity: int) -> Tuple[bool, str, int]:
        """
        STATIC METHOD:
        =============
        Validate group size input.
        
        Parameters:
            size_str: The group size as a string
            max_capacity: Maximum allowed capacity
            
        Returns:
            Tuple (is_valid, error_message, size_as_int)
        """
        # Check if empty
        if not size_str:
            return (False, "Group size cannot be empty", 0)
        
        # Check if it's a number
        try:
            size = int(size_str)
        except ValueError:
            return (False, "Group size must be a number", 0)
        
        # Check if positive
        if size < 1:
            return (False, "Group size must be at least 1", 0)
        
        # Check against max capacity
        if size > max_capacity:
            return (False, f"Group size exceeds room capacity of {max_capacity}", size)
        
        return (True, "", size)
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        STATIC METHOD:
        =============
        Sanitize user input by stripping whitespace and removing dangerous characters.
        
        Parameters:
            input_str: Raw user input
            
        Returns:
            Cleaned string
        """
        if not input_str:
            return ""
        
        # Strip leading/trailing whitespace
        cleaned = input_str.strip()
        
        # Limit length
        if len(cleaned) > 200:
            cleaned = cleaned[:200]
        
        return cleaned


# =============================================================================
# CLASS: DateTimeUtils
# =============================================================================
# Utility class for date and time operations.
# =============================================================================
class DateTimeUtils:
    """
    Utility class for date and time operations.
    """
    
    @staticmethod
    def get_current_datetime() -> datetime:
        """
        STATIC METHOD:
        =============
        Get the current date and time.
        """
        return datetime.now()
    
    @staticmethod
    def get_current_date_string() -> str:
        """
        STATIC METHOD:
        =============
        Get today's date as a string in YYYY-MM-DD format.
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_time_string() -> str:
        """
        STATIC METHOD:
        =============
        Get current time as a string in HH:MM format.
        """
        return datetime.now().strftime("%H:%M")
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M") -> str:
        """
        STATIC METHOD:
        =============
        Format a datetime object to string.
        
        Parameters:
            dt: datetime object
            format_str: Format string (default: YYYY-MM-DD HH:MM)
            
        Returns:
            Formatted string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M") -> Optional[datetime]:
        """
        STATIC METHOD:
        =============
        Parse a string to datetime object.
        
        Parameters:
            datetime_str: String to parse
            format_str: Expected format
            
        Returns:
            datetime object or None if parsing fails
        """
        try:
            return datetime.strptime(datetime_str, format_str)
        except ValueError:
            return None
    
    @staticmethod
    def get_time_slots_for_date(date_str: str, start_hour: int = 8, end_hour: int = 22, 
                                 slot_minutes: int = 60) -> List[str]:
        """
        STATIC METHOD:
        =============
        Generate available time slots for a given date.
        Useful for dropdown menus in the GUI.
        
        Parameters:
            date_str: Date in YYYY-MM-DD format
            start_hour: First hour of availability (default 8 AM)
            end_hour: Last hour of availability (default 10 PM)
            slot_minutes: Duration of each slot (default 60 minutes)
            
        Returns:
            List of time slot strings
        """
        slots = []
        
        try:
            base_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return slots
        
        current = base_date.replace(hour=start_hour, minute=0)
        end = base_date.replace(hour=end_hour, minute=0)
        
        while current < end:
            slot_str = current.strftime("%H:%M")
            slots.append(slot_str)
            current += timedelta(minutes=slot_minutes)
        
        return slots
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """
        STATIC METHOD:
        =============
        Check if a date string is valid.
        
        Parameters:
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_time(time_str: str) -> bool:
        """
        STATIC METHOD:
        =============
        Check if a time string is valid.
        
        Parameters:
            time_str: Time in HH:MM format
            
        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False


# =============================================================================
# CLASS: FormatUtils
# =============================================================================
# Utility class for formatting output strings.
# =============================================================================
class FormatUtils:
    """
    Utility class for formatting output for display.
    """
    
    @staticmethod
    def format_room_info(room) -> str:
        """
        STATIC METHOD:
        =============
        Format room information for display.
        
        Parameters:
            room: An AbstractRoom object
            
        Returns:
            Formatted string with room details
        """
        return (f"{room.room_number} - {room.get_room_type()}\n"
                f"  Location: {room.location}\n"
                f"  Capacity: {room.capacity} people\n"
                f"  {room.get_rules()}")
    
    @staticmethod
    def format_reservation_info(reservation) -> str:
        """
        STATIC METHOD:
        =============
        Format reservation information for display.
        
        Parameters:
            reservation: A Reservation object
            
        Returns:
            Formatted string with reservation details
        """
        return (f"Reservation ID: {reservation.reservation_id}\n"
                f"Room: {reservation.room.room_number} ({reservation.room.get_room_type()})\n"
                f"Time: {reservation.time_slot}\n"
                f"Group Size: {reservation.group_size}\n"
                f"Status: {reservation.status}")
    
    @staticmethod
    def truncate_string(text: str, max_length: int = 50) -> str:
        """
        STATIC METHOD:
        =============
        Truncate a string to a maximum length.
        
        Parameters:
            text: Input string
            max_length: Maximum allowed length
            
        Returns:
            Truncated string with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."


# =============================================================================
# Standalone utility functions (not in a class)
# These are simple helper functions that don't need OOP structure.
# =============================================================================

def generate_sample_dates(days: int = 7) -> List[str]:
    """
    Generate a list of future dates for dropdown menus.
    
    Parameters:
        days: Number of days to generate (default 7)
        
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    dates = []
    today = datetime.now()
    
    for i in range(days):
        future_date = today + timedelta(days=i)
        dates.append(future_date.strftime("%Y-%m-%d"))
    
    return dates


def get_room_type_choices() -> List[str]:
    """
    Get the list of room type choices for dropdown menus.
    
    Returns:
        List of room type display names
    """
    return [
        "Study Room (自習室)",
        "Discussion Room (討論室)",
        "Sports Room (運動室)"
    ]


def get_room_type_short(room_type: str) -> str:
    """
    Get a short code for a room type.
    
    Parameters:
        room_type: Full room type name
        
    Returns:
        Short code (e.g., "Study" -> "SR")
    """
    mapping = {
        "Study Room (自習室)": "Study",
        "Discussion Room (討論室)": "Discussion",
        "Sports Room (運動室)": "Sports"
    }
    return mapping.get(room_type, "Unknown")


def validate_capacity_for_room_type(capacity: int, room_type: str) -> Tuple[bool, str]:
    """
    Validate capacity based on room type constraints.
    
    Parameters:
        capacity: Requested capacity
        room_type: Type of room
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if "Study" in room_type:
        if capacity < 1:
            return (False, "Study rooms require at least 1 person")
        if capacity > 4:
            return (False, "Study rooms max capacity is 4")
    
    elif "Discussion" in room_type:
        if capacity < 2:
            return (False, "Discussion rooms require at least 2 people")
        if capacity > 8:
            return (False, "Discussion rooms max capacity is 8")
    
    elif "Sports" in room_type:
        if capacity < 1:
            return (False, "Sports rooms require at least 1 person")
        if capacity > 20:
            return (False, "Sports rooms max capacity is 20")
    
    return (True, "")
