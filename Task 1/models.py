"""
models.py
=========
This module defines all data models for the Campus Multi-Room Reservation System.
It demonstrates Abstract Data Types (ADT), Inheritance, Polymorphism, Encapsulation,
Class/Object instantiation, Instance Variables, Methods, Constructors, Class Variables,
and Static Methods.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


# =============================================================================
# ABSTRACT DATA TYPE (ADT): AbstractRoom
# =============================================================================
# ADT: Using ABC (Abstract Base Class) to define a template that all room types
# must follow. This enforces a contract - any class inheriting from AbstractRoom
# MUST implement the abstract methods.
# =============================================================================
class AbstractRoom(ABC):
    """
    Abstract Base Class representing a generic room in the campus.
    This is an Abstract Data Type that defines the interface for all room types.
    """
    
    # ==========================================================================
    # CLASS VARIABLE: Shared across ALL room instances
    # ==========================================================================
    # This variable is shared by all subclasses and instances.
    # It tracks the total count of rooms created in the system.
    # ==========================================================================
    _total_rooms_count: int = 0
    
    def __init__(self, room_number: str, capacity: int, location: str):
        """
        CONSTRUCTOR (__init__):
        =======================
        Initializes a new room object with instance-specific data.
        This method runs automatically when a new room is created.
        
        Parameters:
            room_number: Unique identifier for the room (e.g., "SR-101")
            capacity: Maximum number of people allowed
            location: Building and floor information
        """
        # ======================================================================
        # ENCAPSULATION: Using single underscore prefix to indicate "protected"
        # These attributes should not be accessed directly from outside.
        # Use getter/setter methods or @property to access them safely.
        # ======================================================================
        self._room_number = room_number      # Protected: Room identifier
        self._capacity = capacity            # Protected: Max people allowed
        self._location = location            # Protected: Physical location
        self._is_available = True            # Protected: Availability status
        self._reservations: List['Reservation'] = []  # Protected: List of bookings
        
        # Increment class variable (shared across all instances)
        AbstractRoom._total_rooms_count += 1
    
    # ==========================================================================
    # ENCAPSULATION: @property decorators for controlled attribute access
    # These act as "getters" - they allow reading private/protected attributes
    # while preventing direct modification from outside the class.
    # ==========================================================================
    @property
    def room_number(self) -> str:
        """Getter for room_number - allows reading but not direct setting."""
        return self._room_number
    
    @property
    def capacity(self) -> int:
        """Getter for capacity - controlled access to the attribute."""
        return self._capacity
    
    @property
    def location(self) -> str:
        """Getter for location."""
        return self._location
    
    @property
    def is_available(self) -> bool:
        """Getter for availability status."""
        return self._is_available
    
    @property
    def reservations(self) -> List['Reservation']:
        """Getter for reservations list - returns a copy to prevent external modification."""
        return self._reservations.copy()
    
    # ==========================================================================
    # CLASS METHOD / STATIC METHOD: Accessing class-level data
    # ==========================================================================
    @classmethod
    def get_total_rooms_count(cls) -> int:
        """
        CLASS METHOD:
        =============
        Returns the total number of rooms created across all types.
        This method operates on the class itself, not on instances.
        """
        return cls._total_rooms_count
    
    # ==========================================================================
    # ABSTRACT METHODS: Must be implemented by all concrete subclasses
    # ==========================================================================
    # These methods define the interface that all room types must provide.
    # The actual implementation will vary by room type (Polymorphism).
    # ==========================================================================
    
    @abstractmethod
    def book(self, reservation: 'Reservation') -> bool:
        """
        ABSTRACT METHOD:
        ================
        Book this room for a reservation. Each room type implements this differently.
        Must be overridden by concrete subclasses.
        
        Parameters:
            reservation: The reservation object to book
            
        Returns:
            True if booking successful, False otherwise
        """
        pass
    
    @abstractmethod
    def cancel(self, reservation: 'Reservation') -> bool:
        """
        ABSTRACT METHOD:
        ================
        Cancel a reservation for this room. Must be implemented by subclasses.
        
        Parameters:
            reservation: The reservation to cancel
            
        Returns:
            True if cancellation successful, False otherwise
        """
        pass
    
    @abstractmethod
    def check_availability(self, time_slot: 'TimeSlot') -> bool:
        """
        ABSTRACT METHOD:
        ================
        Check if the room is available for a given time slot.
        Each room type may have different rules (Polymorphism).
        
        Parameters:
            time_slot: The time period to check
            
        Returns:
            True if available, False otherwise
        """
        pass
    
    @abstractmethod
    def get_room_type(self) -> str:
        """
        ABSTRACT METHOD:
        ================
        Returns the type of room as a string.
        Each subclass must implement this to identify itself.
        """
        pass
    
    @abstractmethod
    def get_rules(self) -> str:
        """
        ABSTRACT METHOD:
        ================
        Returns a string describing the specific rules for this room type.
        Each room type has different rules.
        """
        pass
    
    # ==========================================================================
    # INSTANCE METHOD: Shared functionality across all room types
    # ==========================================================================
    def has_conflict(self, time_slot: 'TimeSlot') -> bool:
        """
        INSTANCE METHOD:
        ================
        Check if a given time slot conflicts with any existing reservation.
        This method operates on instance data (self._reservations).
        
        Parameters:
            time_slot: The time period to check for conflicts
            
        Returns:
            True if there's a conflict, False otherwise
        """
        # Iterate through all reservations and check for time overlap
        for reservation in self._reservations:
            if reservation.time_slot.overlaps_with(time_slot):
                return True
        return False
    
    def __str__(self) -> str:
        """
        INSTANCE METHOD (magic method):
        ================================
        Returns a string representation of the room.
        This is called when you print(room) or str(room).
        """
        return f"{self.get_room_type()} {self._room_number} (Capacity: {self._capacity})"


# =============================================================================
# INHERITANCE: StudyRoom extends AbstractRoom
# =============================================================================
# This class inherits from AbstractRoom and provides concrete implementations
# of all abstract methods. It represents a quiet study room.
# =============================================================================
class StudyRoom(AbstractRoom):
    """
    Concrete class representing a Study Room (自習室).
    Inherits from AbstractRoom and implements study-specific rules.
    """
    
    # ==========================================================================
    # CLASS VARIABLE: Specific to StudyRoom class
    # ==========================================================================
    _quiet_hours_required: bool = True  # All study rooms require quiet hours
    
    def __init__(self, room_number: str, capacity: int, location: str, 
                 has_whiteboard: bool = False):
        """
        CONSTRUCTOR (Extended):
        =======================
        Initializes a StudyRoom with additional study-specific attributes.
        Calls the parent class constructor using super().
        
        Parameters:
            room_number: Unique room identifier
            capacity: Maximum people (usually 1-4 for study rooms)
            location: Building and floor
            has_whiteboard: Whether the room has a whiteboard
        """
        # Call parent constructor - INHERITANCE in action
        super().__init__(room_number, capacity, location)
        
        # StudyRoom-specific instance variables
        self._has_whiteboard = has_whiteboard
        self._quiet_rule_enforced = True  # Study rooms are always quiet
    
    # ==========================================================================
    # ENCAPSULATION: Getter for study-specific attributes
    # ==========================================================================
    @property
    def has_whiteboard(self) -> bool:
        """Getter for whiteboard availability."""
        return self._has_whiteboard
    
    # ==========================================================================
    # POLYMORPHISM: Different implementation of abstract methods
    # ==========================================================================
    # Each room type implements these methods differently based on their rules.
    # This is the essence of Polymorphism - same interface, different behavior.
    # ==========================================================================
    
    def book(self, reservation: 'Reservation') -> bool:
        """
        POLYMORPHISM: StudyRoom-specific booking logic.
        Study rooms require quiet confirmation and have strict capacity limits.
        """
        # Check if room is available for the time slot
        if not self.check_availability(reservation.time_slot):
            return False
        
        # Study room specific: Check if user acknowledged quiet rules
        # (In real implementation, this would be checked in GUI)
        if reservation.group_size > self._capacity:
            return False
        
        # Add reservation to the list
        self._reservations.append(reservation)
        return True
    
    def cancel(self, reservation: 'Reservation') -> bool:
        """
        POLYMORPHISM: StudyRoom-specific cancellation logic.
        """
        if reservation in self._reservations:
            self._reservations.remove(reservation)
            return True
        return False
    
    def check_availability(self, time_slot: 'TimeSlot') -> bool:
        """
        POLYMORPHISM: StudyRoom-specific availability check.
        Study rooms have standard availability checking.
        """
        # Check for time conflicts
        if self.has_conflict(time_slot):
            return False
        
        # Study rooms are available if no conflicts
        return True
    
    def get_room_type(self) -> str:
        """POLYMORPHISM: Returns the room type identifier."""
        return "Study Room (自習室)"
    
    def get_rules(self) -> str:
        """POLYMORPHISM: Returns study room specific rules."""
        return ("Rules: 1) Maintain silence at all times. "
                f"2) Max capacity: {self._capacity} people. "
                f"3) Whiteboard: {'Yes' if self._has_whiteboard else 'No'}")


# =============================================================================
# INHERITANCE: DiscussionRoom extends AbstractRoom
# =============================================================================
class DiscussionRoom(AbstractRoom):
    """
    Concrete class representing a Discussion Room (討論室).
    Allows group discussions with audio/visual equipment.
    """
    
    # Class constant for discussion rooms
    MAX_CAPACITY: int = 8  # Discussion rooms have strict max limit
    
    def __init__(self, room_number: str, capacity: int, location: str,
                 has_projector: bool = True, has_audio_system: bool = True):
        """
        CONSTRUCTOR: Initialize DiscussionRoom with AV equipment info.
        """
        # Validate capacity for discussion rooms
        if capacity > self.MAX_CAPACITY:
            capacity = self.MAX_CAPACITY
            
        super().__init__(room_number, capacity, location)
        self._has_projector = has_projector
        self._has_audio_system = has_audio_system
        self._discussion_allowed = True  # Unlike study rooms, discussion is allowed
    
    @property
    def has_projector(self) -> bool:
        """Getter for projector availability."""
        return self._has_projector
    
    @property
    def has_audio_system(self) -> bool:
        """Getter for audio system availability."""
        return self._has_audio_system
    
    def book(self, reservation: 'Reservation') -> bool:
        """
        POLYMORPHISM: DiscussionRoom booking with group size validation.
        Discussion rooms require minimum 2 people (it's a discussion room!).
        """
        if not self.check_availability(reservation.time_slot):
            return False
        
        # Discussion room specific: Minimum 2 people required
        if reservation.group_size < 2:
            return False
            
        # Cannot exceed capacity
        if reservation.group_size > self._capacity:
            return False
        
        self._reservations.append(reservation)
        return True
    
    def cancel(self, reservation: 'Reservation') -> bool:
        """POLYMORPHISM: DiscussionRoom cancellation."""
        if reservation in self._reservations:
            self._reservations.remove(reservation)
            return True
        return False
    
    def check_availability(self, time_slot: 'TimeSlot') -> bool:
        """
        POLYMORPHISM: DiscussionRoom availability.
        Similar to study room but may have different time restrictions.
        """
        return not self.has_conflict(time_slot)
    
    def get_room_type(self) -> str:
        """POLYMORPHISM: Returns room type."""
        return "Discussion Room (討論室)"
    
    def get_rules(self) -> str:
        """POLYMORPHISM: Discussion room specific rules."""
        return (f"Rules: 1) Min 2, Max {self._capacity} people. "
                f"2) Projector: {'Yes' if self._has_projector else 'No'}. "
                f"3) Audio: {'Yes' if self._has_audio_system else 'No'}")


# =============================================================================
# INHERITANCE: SportsRoom extends AbstractRoom
# =============================================================================
class SportsRoom(AbstractRoom):
    """
    Concrete class representing a Sports Room (運動室).
    For physical activities and exercise.
    """
    
    def __init__(self, room_number: str, capacity: int, location: str,
                 equipment_list: List[str] = None, requires_equipment_check: bool = True):
        """
        CONSTRUCTOR: Initialize SportsRoom with equipment information.
        
        Parameters:
            equipment_list: List of available equipment (e.g., ["yoga mats", "balls"])
            requires_equipment_check: Whether equipment must be checked before booking
        """
        super().__init__(room_number, capacity, location)
        self._equipment_list = equipment_list or []
        self._requires_equipment_check = requires_equipment_check
        self._equipment_checked = False  # Flag to track if equipment is checked
    
    @property
    def equipment_list(self) -> List[str]:
        """Getter for available equipment list."""
        return self._equipment_list.copy()
    
    @property
    def requires_equipment_check(self) -> bool:
        """Getter for equipment check requirement."""
        return self._requires_equipment_check
    
    def set_equipment_checked(self, checked: bool) -> None:
        """
        ENCAPSULATION: Controlled setter for equipment check status.
        This method allows external code to mark equipment as checked.
        """
        self._equipment_checked = checked
    
    def book(self, reservation: 'Reservation') -> bool:
        """
        POLYMORPHISM: SportsRoom booking with equipment check requirement.
        Sports rooms require equipment verification before booking.
        """
        if not self.check_availability(reservation.time_slot):
            return False
        
        # Sports room specific: Equipment must be checked if required
        if self._requires_equipment_check and not self._equipment_checked:
            # In real implementation, this would trigger equipment check workflow
            pass  # Allow booking but flag for equipment check
        
        # Check group size against capacity
        if reservation.group_size > self._capacity:
            return False
        
        self._reservations.append(reservation)
        return True
    
    def cancel(self, reservation: 'Reservation') -> bool:
        """POLYMORPHISM: SportsRoom cancellation."""
        if reservation in self._reservations:
            self._reservations.remove(reservation)
            return True
        return False
    
    def check_availability(self, time_slot: 'TimeSlot') -> bool:
        """
        POLYMORPHISM: SportsRoom availability with safety buffer.
        Sports rooms may need cleanup time between sessions.
        """
        # Check for conflicts with 15-minute buffer for cleanup
        for reservation in self._reservations:
            if reservation.time_slot.overlaps_with_buffer(time_slot, buffer_minutes=15):
                return False
        return True
    
    def get_room_type(self) -> str:
        """POLYMORPHISM: Returns room type."""
        return "Sports Room (運動室)"
    
    def get_rules(self) -> str:
        """POLYMORPHISM: Sports room specific rules."""
        equipment_str = ", ".join(self._equipment_list) if self._equipment_list else "None"
        return (f"Rules: 1) Max {self._capacity} people. "
                f"2) Equipment: {equipment_str}. "
                f"3) Safety check required: {'Yes' if self._requires_equipment_check else 'No'}")


# =============================================================================
# CLASS: TimeSlot
# =============================================================================
# Represents a time period with start and end datetime.
# Used for reservations and availability checking.
# =============================================================================
class TimeSlot:
    """
    Represents a time range for room reservations.
    """
    
    def __init__(self, start_time: datetime, end_time: datetime):
        """
        CONSTRUCTOR: Initialize a time slot.
        
        Parameters:
            start_time: When the reservation starts
            end_time: When the reservation ends
        """
        # ENCAPSULATION: Private attributes (double underscore)
        # These cannot be accessed directly from outside the class
        self.__start_time = start_time
        self.__end_time = end_time
        
        # Validate that end is after start
        if end_time <= start_time:
            raise ValueError("End time must be after start time")
        
        # Validate that start time is in the future
        if start_time < datetime.now():
            raise ValueError("Cannot create time slots in the past")
    
    # ENCAPSULATION: Property getters for private attributes
    @property
    def start_time(self) -> datetime:
        """Getter for start time."""
        return self.__start_time
    
    @property
    def end_time(self) -> datetime:
        """Getter for end time."""
        return self.__end_time
    
    @property
    def duration_minutes(self) -> int:
        """
        INSTANCE METHOD (property): Calculate duration in minutes.
        This is computed on-demand from instance variables.
        """
        delta = self.__end_time - self.__start_time
        return int(delta.total_seconds() / 60)
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """
        INSTANCE METHOD: Check if this time slot overlaps with another.
        Two time slots overlap if they share any common time period.
        
        Parameters:
            other: Another TimeSlot to compare with
            
        Returns:
            True if there's an overlap, False otherwise
        """
        # Two intervals overlap if:
        # start1 < end2 AND start2 < end1
        return (self.__start_time < other.__end_time and 
                other.__start_time < self.__end_time)
    
    def overlaps_with_buffer(self, other: 'TimeSlot', buffer_minutes: int = 15) -> bool:
        """
        INSTANCE METHOD: Check overlap with a buffer time (for cleanup/prep).
        Used by SportsRoom to ensure cleanup time between sessions.
        
        Parameters:
            other: Another TimeSlot to compare
            buffer_minutes: Extra time to add before and after this slot
            
        Returns:
            True if there's an overlap including buffer
        """
        from datetime import timedelta
        
        # Create adjusted times with buffer
        buffered_start = self.__start_time - timedelta(minutes=buffer_minutes)
        buffered_end = self.__end_time + timedelta(minutes=buffer_minutes)
        
        # Check overlap with buffered times
        return (buffered_start < other.__end_time and 
                other.__start_time < buffered_end)
    
    def __str__(self) -> str:
        """String representation of the time slot."""
        format_str = "%Y-%m-%d %H:%M"
        return f"{self.__start_time.strftime(format_str)} to {self.__end_time.strftime(format_str)}"


# =============================================================================
# CLASS: User
# =============================================================================
# Represents a student user in the system.
# =============================================================================
class User:
    """
    Represents a university student who can make reservations.
    """
    
    # Class variable: Pre-existing valid student IDs (simulating database)
    # In a real system, this would be in a database
    _valid_student_ids: set = set()
    
    def __init__(self, student_id: str, name: str = ""):
        """
        CONSTRUCTOR: Initialize a User.
        
        Parameters:
            student_id: 8-digit student ID
            name: Student's name (optional for this system)
        """
        # ENCAPSULATION: Protected attributes
        self._student_id = student_id
        self._name = name or f"Student_{student_id}"
        self._reservations: List['Reservation'] = []  # User's reservations
        
        # Add to valid IDs (simulating pre-existing users)
        User._valid_student_ids.add(student_id)
    
    # ENCAPSULATION: Property getters
    @property
    def student_id(self) -> str:
        """Getter for student ID."""
        return self._student_id
    
    @property
    def name(self) -> str:
        """Getter for student name."""
        return self._name
    
    # ==========================================================================
    # INSTANCE METHODS: User behaviors
    # ==========================================================================
    def add_reservation(self, reservation: 'Reservation') -> None:
        """
        INSTANCE METHOD: Add a reservation to this user's list.
        Demonstrates how objects interact with each other.
        """
        self._reservations.append(reservation)
    
    def remove_reservation(self, reservation: 'Reservation') -> bool:
        """
        INSTANCE METHOD: Remove a reservation from this user's list.
        """
        if reservation in self._reservations:
            self._reservations.remove(reservation)
            return True
        return False
    
    def get_reservations(self) -> List['Reservation']:
        """
        INSTANCE METHOD: Get all reservations for this user.
        Returns a copy to prevent external modification.
        """
        return self._reservations.copy()
    
    # ==========================================================================
    # STATIC METHOD: Validation without needing an instance
    # ==========================================================================
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """
        STATIC METHOD:
        =============
        Validates that a student ID is exactly 8 digits.
        This method doesn't need a User instance - it operates on the parameter only.
        
        Parameters:
            student_id: The ID to validate
            
        Returns:
            True if valid (exactly 8 digits), False otherwise
        """
        if not student_id:
            return False
        if len(student_id) != 8:
            return False
        if not student_id.isdigit():
            return False
        return True
    
    @classmethod
    def is_valid_student_id(cls, student_id: str) -> bool:
        """
        CLASS METHOD: Check if ID exists in the system.
        """
        return student_id in cls._valid_student_ids
    
    def __str__(self) -> str:
        """String representation of the user."""
        return f"User({self._student_id}, {self._name})"


# =============================================================================
# CLASS: Reservation
# =============================================================================
# Represents a booking of a room by a user for a specific time.
# =============================================================================
class Reservation:
    """
    Represents a reservation linking a User, Room, and TimeSlot.
    """
    
    # Class variable: Auto-incrementing reservation ID counter
    _reservation_counter: int = 0
    
    def __init__(self, user: User, room: AbstractRoom, time_slot: TimeSlot, 
                 group_size: int = 1, purpose: str = ""):
        """
        CONSTRUCTOR: Initialize a Reservation.
        
        Parameters:
            user: The User making the reservation
            room: The AbstractRoom being reserved
            time_slot: The TimeSlot of the reservation
            group_size: Number of people (default 1)
            purpose: Purpose of the reservation (optional)
        """
        # Generate unique reservation ID
        Reservation._reservation_counter += 1
        self.__reservation_id = f"RES-{Reservation._reservation_counter:04d}"
        
        # Store references to related objects
        self.__user = user
        self.__room = room
        self.__time_slot = time_slot
        self.__group_size = group_size
        self.__purpose = purpose
        self.__created_at = datetime.now()
        self.__status = "active"  # active, cancelled, completed
    
    # ENCAPSULATION: Comprehensive property getters
    @property
    def reservation_id(self) -> str:
        """Getter for unique reservation ID."""
        return self.__reservation_id
    
    @property
    def user(self) -> User:
        """Getter for the user who made this reservation."""
        return self.__user
    
    @property
    def room(self) -> AbstractRoom:
        """Getter for the reserved room."""
        return self.__room
    
    @property
    def time_slot(self) -> TimeSlot:
        """Getter for the time slot."""
        return self.__time_slot
    
    @property
    def group_size(self) -> int:
        """Getter for group size."""
        return self.__group_size
    
    @property
    def status(self) -> str:
        """Getter for reservation status."""
        return self.__status
    
    def cancel(self) -> None:
        """
        INSTANCE METHOD: Mark this reservation as cancelled.
        ENCAPSULATION: Controlled status modification.
        """
        self.__status = "cancelled"
    
    def is_active(self) -> bool:
        """
        INSTANCE METHOD: Check if reservation is still active.
        """
        return self.__status == "active"
    
    def __str__(self) -> str:
        """String representation of the reservation."""
        return (f"Reservation[{self.__reservation_id}] {self.__user.student_id} -> "
                f"{self.__room.room_number} at {self.__time_slot}")
