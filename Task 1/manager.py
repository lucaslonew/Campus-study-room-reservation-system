"""
manager.py
==========
This module contains the ReservationManager class which handles all business logic
for the Campus Multi-Room Reservation System. It demonstrates OOP concepts including
Singleton pattern (optional), Class Variables, Static Methods, and Object Composition.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Type
from models import (
    AbstractRoom, StudyRoom, DiscussionRoom, SportsRoom, 
    User, Reservation, TimeSlot
)


# =============================================================================
# CLASS: ReservationManager
# =============================================================================
# This class manages all rooms, users, and reservations in the system.
# It acts as a central controller for the application logic.
# =============================================================================
class ReservationManager:
    """
    Central manager for the reservation system.
    Handles all CRUD operations for rooms, users, and reservations.
    """
    
    # ==========================================================================
    # CLASS VARIABLES: Shared data across all manager instances
    # ==========================================================================
    # These variables store the entire state of the system in memory.
    # They are shared across all instances of ReservationManager.
    # ==========================================================================
    _all_rooms: List[AbstractRoom] = []           # All rooms in the system
    _all_users: Dict[str, User] = {}              # Map of student_id -> User
    _all_reservations: List[Reservation] = []     # All reservations made
    
    # Track if sample data has been initialized (to avoid duplicates)
    _initialized: bool = False
    
    def __init__(self):
        """
        CONSTRUCTOR: Initialize the ReservationManager.
        If sample data hasn't been loaded yet, it initializes the system
        with pre-created rooms and sample users.
        """
        # Initialize sample data only once (using class variable check)
        if not ReservationManager._initialized:
            self._initialize_sample_data()
            ReservationManager._initialized = True
    
    # ==========================================================================
    # INSTANCE METHOD: Initialize sample data for demonstration
    # ==========================================================================
    def _initialize_sample_data(self) -> None:
        """
        INSTANCE METHOD: Create sample rooms and users for testing.
        This populates the system with initial data so the application
        is usable immediately without manual data entry.
        """
        # Create Study Rooms (自習室) - quiet individual study spaces
        study_rooms = [
            StudyRoom("SR-101", 1, "Library 1F", has_whiteboard=False),
            StudyRoom("SR-102", 2, "Library 1F", has_whiteboard=True),
            StudyRoom("SR-103", 4, "Library 2F", has_whiteboard=True),
            StudyRoom("SR-201", 1, "Science Building 3F", has_whiteboard=False),
            StudyRoom("SR-202", 2, "Science Building 3F", has_whiteboard=True),
        ]
        
        # Create Discussion Rooms (討論室) - group meeting spaces
        discussion_rooms = [
            DiscussionRoom("DR-101", 4, "Library 2F", has_projector=True, has_audio_system=True),
            DiscussionRoom("DR-102", 6, "Library 2F", has_projector=True, has_audio_system=False),
            DiscussionRoom("DR-103", 8, "Library 3F", has_projector=True, has_audio_system=True),
            DiscussionRoom("DR-201", 4, "Engineering Building 1F", has_projector=True, has_audio_system=True),
            DiscussionRoom("DR-202", 6, "Engineering Building 2F", has_projector=False, has_audio_system=True),
        ]
        
        # Create Sports Rooms (運動室) - exercise and activity spaces
        sports_rooms = [
            SportsRoom("SP-101", 10, "Gymnasium 1F", 
                      equipment_list=["yoga mats", "exercise balls"], 
                      requires_equipment_check=True),
            SportsRoom("SP-102", 15, "Gymnasium 1F", 
                      equipment_list=["basketballs", "volleyballs"], 
                      requires_equipment_check=True),
            SportsRoom("SP-103", 8, "Gymnasium 2F", 
                      equipment_list=["table tennis tables"], 
                      requires_equipment_check=True),
            SportsRoom("SP-201", 20, "Sports Center B1", 
                      equipment_list=["badminton nets", "shuttlecocks"], 
                      requires_equipment_check=True),
            SportsRoom("SP-202", 6, "Sports Center 1F", 
                      equipment_list=["dance mirrors", "sound system"], 
                      requires_equipment_check=False),
        ]
        
        # Add all rooms to the class-level list
        ReservationManager._all_rooms.extend(study_rooms)
        ReservationManager._all_rooms.extend(discussion_rooms)
        ReservationManager._all_rooms.extend(sports_rooms)
        
        # Create sample users (pre-existing in the system)
        sample_users = [
            User("12345678", "Alice Chen"),
            User("87654321", "Bob Wang"),
            User("11111111", "Carol Liu"),
            User("22222222", "David Zhang"),
            User("33333333", "Emma Li"),
        ]
        
        # Add users to the dictionary for quick lookup by student ID
        for user in sample_users:
            ReservationManager._all_users[user.student_id] = user
    
    # ==========================================================================
    # STATIC METHODS: Utility functions that don't need instance state
    # ==========================================================================
    @staticmethod
    def get_room_types() -> List[str]:
        """
        STATIC METHOD:
        =============
        Returns a list of available room type names.
        This method doesn't need an instance - it just returns constant data.
        
        Returns:
            List of room type display names
        """
        return ["Study Room (自習室)", "Discussion Room (討論室)", "Sports Room (運動室)"]
    
    @staticmethod
    def parse_datetime(date_string: str) -> Optional[datetime]:
        """
        STATIC METHOD:
        =============
        Parse a datetime string in format "YYYY-MM-DD HH:MM".
        Returns None if parsing fails.
        
        Parameters:
            date_string: String in format "YYYY-MM-DD HH:MM"
            
        Returns:
            datetime object or None if invalid format
        """
        try:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """
        STATIC METHOD:
        =============
        Format a datetime object as "YYYY-MM-DD HH:MM".
        
        Parameters:
            dt: datetime object to format
            
        Returns:
            Formatted string
        """
        return dt.strftime("%Y-%m-%d %H:%M")
    
    # ==========================================================================
    # INSTANCE METHODS: User management
    # ==========================================================================
    def get_or_create_user(self, student_id: str) -> Optional[User]:
        """
        INSTANCE METHOD:
        ================
        Get an existing user or create a new one if valid ID.
        
        Parameters:
            student_id: 8-digit student ID
            
        Returns:
            User object if ID is valid, None otherwise
        """
        # Validate the student ID format
        if not User.validate_student_id(student_id):
            return None
        
        # Check if user already exists
        if student_id in ReservationManager._all_users:
            return ReservationManager._all_users[student_id]
        
        # Create new user (simulating pre-existing user validation)
        # In this system, we accept any valid 8-digit ID as a pre-existing user
        new_user = User(student_id)
        ReservationManager._all_users[student_id] = new_user
        return new_user
    
    def get_user(self, student_id: str) -> Optional[User]:
        """
        INSTANCE METHOD: Get a user by student ID.
        """
        return ReservationManager._all_users.get(student_id)
    
    # ==========================================================================
    # INSTANCE METHODS: Room search and filtering
    # ==========================================================================
    def get_all_rooms(self) -> List[AbstractRoom]:
        """
        INSTANCE METHOD: Get all rooms in the system.
        Returns a copy to prevent external modification.
        """
        return ReservationManager._all_rooms.copy()
    
    def get_rooms_by_type(self, room_type: str) -> List[AbstractRoom]:
        """
        INSTANCE METHOD:
        ================
        Filter rooms by their type.
        
        Parameters:
            room_type: String like "Study Room (自習室)" or just "Study"
            
        Returns:
            List of rooms matching the type
        """
        result = []
        for room in ReservationManager._all_rooms:
            # Check if room type matches (partial match allowed)
            if room_type.lower() in room.get_room_type().lower():
                result.append(room)
        return result
    
    def search_available_rooms(self, room_type: str, time_slot: TimeSlot, 
                               min_capacity: int = 1) -> List[AbstractRoom]:
        """
        INSTANCE METHOD:
        ================
        Search for available rooms matching criteria.
        This is the main search function used by the GUI.
        
        Parameters:
            room_type: Type of room to search for
            time_slot: Desired time period
            min_capacity: Minimum capacity required
            
        Returns:
            List of available rooms matching all criteria
        """
        available_rooms = []
        
        # Get rooms of the specified type
        rooms_of_type = self.get_rooms_by_type(room_type)
        
        # Filter by availability and capacity
        for room in rooms_of_type:
            # Check capacity requirement
            if room.capacity < min_capacity:
                continue
            
            # Check availability for the time slot
            # POLYMORPHISM: Different room types check availability differently
            if room.check_availability(time_slot):
                available_rooms.append(room)
        
        return available_rooms
    
    def get_room_by_number(self, room_number: str) -> Optional[AbstractRoom]:
        """
        INSTANCE METHOD: Find a room by its room number.
        """
        for room in ReservationManager._all_rooms:
            if room.room_number == room_number:
                return room
        return None
    
    # ==========================================================================
    # INSTANCE METHODS: Reservation operations
    # ==========================================================================
    def make_reservation(self, user: User, room: AbstractRoom, 
                         time_slot: TimeSlot, group_size: int = 1, 
                         purpose: str = "") -> tuple:
        """
        INSTANCE METHOD:
        ================
        Create a new reservation.
        
        Parameters:
            user: The User making the reservation
            room: The Room to reserve
            time_slot: The TimeSlot for the reservation
            group_size: Number of people
            purpose: Purpose of the reservation
            
        Returns:
            Tuple of (success: bool, message: str, reservation: Optional[Reservation])
        """
        # Validate inputs
        if user is None:
            return (False, "User not found", None)
        
        if room is None:
            return (False, "Room not found", None)
        
        if time_slot is None:
            return (False, "Invalid time slot", None)
        
        # Validate group size
        if group_size < 1:
            return (False, "Group size must be at least 1", None)
        
        if group_size > room.capacity:
            return (False, f"Group size ({group_size}) exceeds room capacity ({room.capacity})", None)
        
        # Check for time conflicts
        if not room.check_availability(time_slot):
            return (False, "Room is not available for the selected time", None)
        
        # Create the reservation object
        reservation = Reservation(user, room, time_slot, group_size, purpose)
        
        # POLYMORPHISM: Call the room's book method (different for each room type)
        success = room.book(reservation)
        
        if success:
            # Add to user's reservation list
            user.add_reservation(reservation)
            
            # Add to global reservation list
            ReservationManager._all_reservations.append(reservation)
            
            return (True, f"Reservation successful! ID: {reservation.reservation_id}", reservation)
        else:
            return (False, "Failed to book room (room-specific rules not met)", None)
    
    def cancel_reservation(self, user: User, reservation_id: str) -> tuple:
        """
        INSTANCE METHOD:
        ================
        Cancel a reservation by ID.
        
        Parameters:
            user: The User requesting cancellation
            reservation_id: The ID of the reservation to cancel
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Find the reservation
        reservation = None
        for res in ReservationManager._all_reservations:
            if res.reservation_id == reservation_id:
                reservation = res
                break
        
        if reservation is None:
            return (False, "Reservation not found")
        
        # Verify that the user owns this reservation
        if reservation.user.student_id != user.student_id:
            return (False, "You can only cancel your own reservations")
        
        # Check if already cancelled
        if not reservation.is_active():
            return (False, "Reservation is already cancelled")
        
        # POLYMORPHISM: Call the room's cancel method
        room = reservation.room
        success = room.cancel(reservation)
        
        if success:
            # Mark reservation as cancelled
            reservation.cancel()
            
            # Remove from user's list
            user.remove_reservation(reservation)
            
            return (True, f"Reservation {reservation_id} cancelled successfully")
        else:
            return (False, "Failed to cancel reservation")
    
    def get_user_reservations(self, user: User) -> List[Reservation]:
        """
        INSTANCE METHOD:
        ================
        Get all active reservations for a user.
        
        Parameters:
            user: The User to get reservations for
            
        Returns:
            List of active Reservation objects
        """
        if user is None:
            return []
        
        # Get from user's own list (which is already filtered)
        all_user_reservations = user.get_reservations()
        
        # Filter to only active ones
        active_reservations = [res for res in all_user_reservations if res.is_active()]
        
        # Sort by start time
        active_reservations.sort(key=lambda r: r.time_slot.start_time)
        
        return active_reservations
    
    def get_upcoming_reservations(self, hours: int = 24) -> List[Reservation]:
        """
        INSTANCE METHOD:
        ================
        Get all reservations starting within the next N hours.
        Useful for notifications or reports.
        
        Parameters:
            hours: Number of hours to look ahead
            
        Returns:
            List of upcoming Reservation objects
        """
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        
        upcoming = []
        for reservation in ReservationManager._all_reservations:
            if reservation.is_active():
                start = reservation.time_slot.start_time
                if now <= start <= cutoff:
                    upcoming.append(reservation)
        
        return upcoming
    
    # ==========================================================================
    # CLASS METHODS: Access and modify class-level data
    # ==========================================================================
    @classmethod
    def get_total_rooms(cls) -> int:
        """
        CLASS METHOD:
        =============
        Get the total number of rooms in the system.
        Operates on the class itself, not instances.
        """
        return len(cls._all_rooms)
    
    @classmethod
    def get_total_reservations(cls) -> int:
        """
        CLASS METHOD:
        =============
        Get the total number of reservations made (including cancelled).
        """
        return len(cls._all_reservations)
    
    @classmethod
    def get_statistics(cls) -> Dict[str, int]:
        """
        CLASS METHOD:
        =============
        Get system statistics.
        Returns a dictionary with counts of rooms, users, and reservations.
        """
        return {
            "total_rooms": len(cls._all_rooms),
            "total_users": len(cls._all_users),
            "total_reservations": len(cls._all_reservations),
            "active_reservations": sum(1 for r in cls._all_reservations if r.is_active()),
            "study_rooms": sum(1 for r in cls._all_rooms if isinstance(r, StudyRoom)),
            "discussion_rooms": sum(1 for r in cls._all_rooms if isinstance(r, DiscussionRoom)),
            "sports_rooms": sum(1 for r in cls._all_rooms if isinstance(r, SportsRoom)),
        }
