"""
main.py
=======
Main entry point for the Campus Multi-Room Reservation System.
This module contains the GUI implementation using tkinter and ttk.
It demonstrates OOP concepts including Class/Object instantiation, Inheritance,
Encapsulation, and Event-Driven Programming.

Run this file to start the application: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
from typing import Optional, List

# Import from our custom modules
from models import AbstractRoom, StudyRoom, DiscussionRoom, SportsRoom, User, Reservation, TimeSlot
from manager import ReservationManager
from utils import (
    ValidationUtils, DateTimeUtils, FormatUtils,
    generate_sample_dates, get_room_type_choices, get_room_type_short,
    validate_capacity_for_room_type
)


# =============================================================================
# CLASS: LoginWindow
# =============================================================================
# This class represents the login window where users enter their student ID.
# It demonstrates OOP concepts including Class definition, Instance variables,
# Methods, and Encapsulation.
# =============================================================================
class LoginWindow:
    """
    Login window for the Campus Reservation System.
    Validates 8-digit student ID before allowing access.
    """
    
    def __init__(self, root: tk.Tk, manager: ReservationManager):
        """
        CONSTRUCTOR:
        ============
        Initialize the login window.
        
        Parameters:
            root: The main tkinter window
            manager: The ReservationManager instance for business logic
        """
        # ENCAPSULATION: Store references as instance variables (attributes)
        self._root = root
        self._manager = manager
        self._current_user: Optional[User] = None  # Will store logged-in user
        
        # Configure the main window
        self._root.title("Campus Multi-Room Reservation System - Login")
        self._root.geometry("500x400")
        self._root.resizable(False, False)
        
        # Set up the GUI components
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create and arrange all GUI widgets for the login window.
        Uses ttk for styled widgets.
        """
        # Create main frame with padding
        main_frame = ttk.Frame(self._root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="Campus Multi-Room Reservation System",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="University Room Booking Portal",
            font=("Helvetica", 12)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Icon/Logo placeholder (using a label with text)
        icon_label = ttk.Label(
            main_frame,
            text="📚",
            font=("Helvetica", 48)
        )
        icon_label.pack(pady=(0, 20))
        
        # Login frame
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(fill=tk.X, pady=20)
        
        # Student ID label
        id_label = ttk.Label(
            login_frame,
            text="Student ID (8 digits):",
            font=("Helvetica", 11)
        )
        id_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Student ID entry field
        self._student_id_var = tk.StringVar()
        self._entry_student_id = ttk.Entry(
            login_frame,
            textvariable=self._student_id_var,
            font=("Helvetica", 12),
            width=25
        )
        self._entry_student_id.pack(fill=tk.X, pady=(0, 10))
        self._entry_student_id.focus()  # Set focus to entry
        
        # Hint label
        hint_label = ttk.Label(
            login_frame,
            text="Enter your 8-digit student ID number",
            font=("Helvetica", 9),
            foreground="gray"
        )
        hint_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Login button
        login_button = ttk.Button(
            login_frame,
            text="Login",
            command=self._on_login_click,
            width=20
        )
        login_button.pack(pady=10)
        
        # Bind Enter key to login
        self._entry_student_id.bind("<Return>", lambda e: self._on_login_click())
        
        # Sample IDs label
        sample_label = ttk.Label(
            main_frame,
            text="Sample IDs: 12345678, 87654321, 11111111",
            font=("Helvetica", 9),
            foreground="blue"
        )
        sample_label.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def _on_login_click(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Handle the login button click event.
        Validates the student ID and opens main window if valid.
        """
        # Get the entered student ID
        student_id = self._student_id_var.get().strip()
        
        # Validate using static method from ValidationUtils
        is_valid, error_msg = ValidationUtils.validate_student_id(student_id)
        
        if not is_valid:
            # Show error messagebox and stay on login screen
            messagebox.showerror("Invalid Student ID", error_msg)
            self._student_id_var.set("")  # Clear the entry
            self._entry_student_id.focus()
            return
        
        # Get or create user through the manager
        user = self._manager.get_or_create_user(student_id)
        
        if user is None:
            messagebox.showerror("Error", "Could not create user. Please try again.")
            return
        
        # Store the current user
        self._current_user = user
        
        # Show welcome message
        messagebox.showinfo("Welcome", f"Welcome, {user.name}!\nStudent ID: {user.student_id}")
        
        # Open main window
        self._open_main_window()
    
    def _open_main_window(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Open the main application window and close the login window.
        """
        # Hide the login window
        self._root.withdraw()
        
        # Create new window for main application
        main_window = tk.Toplevel()
        MainWindow(main_window, self._manager, self._current_user, self._root)


# =============================================================================
# CLASS: MainWindow
# =============================================================================
# The main application window with menu options.
# =============================================================================
class MainWindow:
    """
    Main application window with menu options for the reservation system.
    """
    
    def __init__(self, root: tk.Toplevel, manager: ReservationManager, 
                 user: User, login_root: tk.Tk):
        """
        CONSTRUCTOR:
        ============
        Initialize the main window.
        
        Parameters:
            root: The Toplevel window
            manager: ReservationManager instance
            user: Currently logged-in User
            login_root: Reference to the login window root (for logout)
        """
        # ENCAPSULATION: Store instance variables
        self._root = root
        self._manager = manager
        self._current_user = user
        self._login_root = login_root
        
        # Configure window
        self._root.title(f"Campus Reservation System - {user.name}")
        self._root.geometry("600x500")
        self._root.resizable(False, False)
        
        # Handle window close
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create the main menu widgets.
        """
        # Main frame
        main_frame = ttk.Frame(self._root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Welcome header
        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome, {self._current_user.name}!",
            font=("Helvetica", 16, "bold")
        )
        welcome_label.pack(pady=(0, 5))
        
        id_label = ttk.Label(
            main_frame,
            text=f"Student ID: {self._current_user.student_id}",
            font=("Helvetica", 11),
            foreground="gray"
        )
        id_label.pack(pady=(0, 30))
        
        # Menu buttons frame
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button style configuration
        style = ttk.Style()
        style.configure("Menu.TButton", font=("Helvetica", 12), padding=10)
        
        # Search Rooms button
        btn_search = ttk.Button(
            menu_frame,
            text="🔍 Search Available Rooms",
            command=self._open_search_window,
            style="Menu.TButton",
            width=30
        )
        btn_search.pack(pady=8)
        
        # Make Reservation button
        btn_reserve = ttk.Button(
            menu_frame,
            text="📅 Make a Reservation",
            command=self._open_reservation_window,
            style="Menu.TButton",
            width=30
        )
        btn_reserve.pack(pady=8)
        
        # View My Bookings button
        btn_view = ttk.Button(
            menu_frame,
            text="📋 View My Bookings",
            command=self._open_view_bookings_window,
            style="Menu.TButton",
            width=30
        )
        btn_view.pack(pady=8)
        
        # Cancel Reservation button
        btn_cancel = ttk.Button(
            menu_frame,
            text="❌ Cancel Reservation",
            command=self._open_cancel_window,
            style="Menu.TButton",
            width=30
        )
        btn_cancel.pack(pady=8)
        
        # Separator
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=20)
        
        # Logout button
        btn_logout = ttk.Button(
            main_frame,
            text="🚪 Logout",
            command=self._logout,
            width=20
        )
        btn_logout.pack(pady=10)
    
    def _open_search_window(self) -> None:
        """INSTANCE METHOD: Open the search rooms window."""
        search_window = tk.Toplevel(self._root)
        SearchRoomsWindow(search_window, self._manager)
    
    def _open_reservation_window(self) -> None:
        """INSTANCE METHOD: Open the make reservation window."""
        reserve_window = tk.Toplevel(self._root)
        MakeReservationWindow(reserve_window, self._manager, self._current_user)
    
    def _open_view_bookings_window(self) -> None:
        """INSTANCE METHOD: Open the view bookings window."""
        view_window = tk.Toplevel(self._root)
        ViewBookingsWindow(view_window, self._manager, self._current_user)
    
    def _open_cancel_window(self) -> None:
        """INSTANCE METHOD: Open the cancel reservation window."""
        cancel_window = tk.Toplevel(self._root)
        CancelReservationWindow(cancel_window, self._manager, self._current_user)
    
    def _logout(self) -> None:
        """INSTANCE METHOD: Logout and return to login window."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self._root.destroy()
            self._login_root.deiconify()  # Show login window again
    
    def _on_close(self) -> None:
        """INSTANCE METHOD: Handle window close button."""
        self._logout()


# =============================================================================
# CLASS: SearchRoomsWindow
# =============================================================================
# Window for searching available rooms by type, date, time, and capacity.
# =============================================================================
class SearchRoomsWindow:
    """
    Window for searching available rooms with filters.
    """
    
    def __init__(self, root: tk.Toplevel, manager: ReservationManager):
        """
        CONSTRUCTOR:
        ============
        Initialize the search window.
        """
        self._root = root
        self._manager = manager
        
        self._root.title("Search Available Rooms")
        self._root.geometry("700x600")
        self._root.resizable(True, True)
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create search form and results area.
        """
        # Main frame
        main_frame = ttk.Frame(self._root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Search Available Rooms",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Search form frame
        form_frame = ttk.LabelFrame(main_frame, text="Search Criteria", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Room Type
        ttk.Label(form_frame, text="Room Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._room_type_var = tk.StringVar()
        room_types = get_room_type_choices()
        self._room_type_combo = ttk.Combobox(
            form_frame,
            textvariable=self._room_type_var,
            values=room_types,
            state="readonly",
            width=25
        )
        self._room_type_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self._room_type_combo.current(0)  # Select first item
        
        # Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._date_var = tk.StringVar(value=DateTimeUtils.get_current_date_string())
        self._date_entry = ttk.Entry(form_frame, textvariable=self._date_var, width=15)
        self._date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Sample dates dropdown
        sample_dates = generate_sample_dates(7)
        self._date_combo = ttk.Combobox(
            form_frame,
            values=sample_dates,
            state="readonly",
            width=12
        )
        self._date_combo.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self._date_combo.bind("<<ComboboxSelected>>", self._on_date_selected)
        
        # Start Time
        ttk.Label(form_frame, text="Start Time (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self._start_time_var = tk.StringVar(value="09:00")
        self._start_entry = ttk.Entry(form_frame, textvariable=self._start_time_var, width=10)
        self._start_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # End Time
        ttk.Label(form_frame, text="End Time (HH:MM):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self._end_time_var = tk.StringVar(value="10:00")
        self._end_entry = ttk.Entry(form_frame, textvariable=self._end_time_var, width=10)
        self._end_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Capacity
        ttk.Label(form_frame, text="Min Capacity:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self._capacity_var = tk.StringVar(value="1")
        self._capacity_entry = ttk.Entry(form_frame, textvariable=self._capacity_var, width=10)
        self._capacity_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Search button
        search_btn = ttk.Button(
            form_frame,
            text="Search",
            command=self._on_search,
            width=15
        )
        search_btn.grid(row=5, column=0, columnspan=3, pady=15)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Available Rooms", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for results
        columns = ("room_number", "type", "capacity", "location", "rules")
        self._results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        # Define column headings
        self._results_tree.heading("room_number", text="Room #")
        self._results_tree.heading("type", text="Type")
        self._results_tree.heading("capacity", text="Capacity")
        self._results_tree.heading("location", text="Location")
        self._results_tree.heading("rules", text="Rules/Features")
        
        # Set column widths
        self._results_tree.column("room_number", width=80)
        self._results_tree.column("type", width=120)
        self._results_tree.column("capacity", width=60)
        self._results_tree.column("location", width=120)
        self._results_tree.column("rules", width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self._results_tree.yview)
        self._results_tree.configure(yscrollcommand=scrollbar.set)
        
        self._results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self._status_var = tk.StringVar(value="Enter search criteria and click Search")
        status_label = ttk.Label(main_frame, textvariable=self._status_var, foreground="gray")
        status_label.pack(pady=(10, 0))
    
    def _on_date_selected(self, event) -> None:
        """INSTANCE METHOD: Handle date dropdown selection."""
        selected = self._date_combo.get()
        self._date_var.set(selected)
    
    def _on_search(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Handle search button click.
        Validates inputs and displays available rooms.
        """
        # Get values
        room_type = self._room_type_var.get()
        date_str = self._date_var.get().strip()
        start_str = self._start_time_var.get().strip()
        end_str = self._end_time_var.get().strip()
        capacity_str = self._capacity_var.get().strip()
        
        # Validate date
        if not DateTimeUtils.is_valid_date(date_str):
            messagebox.showerror("Invalid Date", "Please enter a valid date (YYYY-MM-DD)")
            return
        
        # Validate times
        if not DateTimeUtils.is_valid_time(start_str):
            messagebox.showerror("Invalid Time", "Please enter a valid start time (HH:MM)")
            return
        
        if not DateTimeUtils.is_valid_time(end_str):
            messagebox.showerror("Invalid Time", "Please enter a valid end time (HH:MM)")
            return
        
        # Create datetime strings
        start_datetime_str = f"{date_str} {start_str}"
        end_datetime_str = f"{date_str} {end_str}"
        
        # Validate datetime range
        is_valid, error_msg, start_dt, end_dt = ValidationUtils.validate_datetime_range(
            start_datetime_str, end_datetime_str
        )
        
        if not is_valid:
            messagebox.showerror("Invalid Time Range", error_msg)
            return
        
        # Validate capacity
        try:
            min_capacity = int(capacity_str)
            if min_capacity < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Capacity", "Capacity must be a positive number")
            return
        
        # Create TimeSlot object
        try:
            time_slot = TimeSlot(start_dt, end_dt)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        # Search for available rooms
        available_rooms = self._manager.search_available_rooms(room_type, time_slot, min_capacity)
        
        # Clear previous results
        for item in self._results_tree.get_children():
            self._results_tree.delete(item)
        
        # Display results
        if not available_rooms:
            self._status_var.set(f"No available {room_type} rooms found for the selected criteria")
            messagebox.showinfo("No Results", "No available rooms found matching your criteria.")
        else:
            for room in available_rooms:
                self._results_tree.insert(
                    "",
                    tk.END,
                    values=(
                        room.room_number,
                        room.get_room_type(),
                        room.capacity,
                        room.location,
                        room.get_rules()[:50] + "..." if len(room.get_rules()) > 50 else room.get_rules()
                    )
                )
            self._status_var.set(f"Found {len(available_rooms)} available room(s)")


# =============================================================================
# CLASS: MakeReservationWindow
# =============================================================================
# Window for making a new reservation.
# =============================================================================
class MakeReservationWindow:
    """
    Window for making a new room reservation.
    """
    
    def __init__(self, root: tk.Toplevel, manager: ReservationManager, user: User):
        """
        CONSTRUCTOR:
        ============
        Initialize the reservation window.
        """
        self._root = root
        self._manager = manager
        self._current_user = user
        self._selected_room: Optional[AbstractRoom] = None
        
        self._root.title("Make a Reservation")
        self._root.geometry("650x700")
        self._root.resizable(False, False)
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create the reservation form.
        """
        # Main frame with scrollbar
        canvas = tk.Canvas(self._root)
        scrollbar = ttk.Scrollbar(self._root, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Main content frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Make a Reservation",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Step 1: Search for rooms
        search_frame = ttk.LabelFrame(main_frame, text="Step 1: Search Criteria", padding="15")
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Room Type
        ttk.Label(search_frame, text="Room Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._room_type_var = tk.StringVar()
        room_types = get_room_type_choices()
        self._room_type_combo = ttk.Combobox(
            search_frame,
            textvariable=self._room_type_var,
            values=room_types,
            state="readonly",
            width=25
        )
        self._room_type_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self._room_type_combo.current(0)
        
        # Date
        ttk.Label(search_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._date_var = tk.StringVar(value=DateTimeUtils.get_current_date_string())
        self._date_entry = ttk.Entry(search_frame, textvariable=self._date_var, width=15)
        self._date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Start Time
        ttk.Label(search_frame, text="Start Time (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self._start_var = tk.StringVar(value="09:00")
        self._start_entry = ttk.Entry(search_frame, textvariable=self._start_var, width=10)
        self._start_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # End Time
        ttk.Label(search_frame, text="End Time (HH:MM):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self._end_var = tk.StringVar(value="10:00")
        self._end_entry = ttk.Entry(search_frame, textvariable=self._end_var, width=10)
        self._end_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Group Size
        ttk.Label(search_frame, text="Group Size:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self._group_var = tk.StringVar(value="1")
        self._group_entry = ttk.Entry(search_frame, textvariable=self._group_var, width=10)
        self._group_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Purpose
        ttk.Label(search_frame, text="Purpose:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self._purpose_var = tk.StringVar()
        self._purpose_entry = ttk.Entry(search_frame, textvariable=self._purpose_var, width=30)
        self._purpose_entry.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Search button
        search_btn = ttk.Button(
            search_frame,
            text="Find Available Rooms",
            command=self._on_find_rooms,
            width=20
        )
        search_btn.grid(row=6, column=0, columnspan=2, pady=15)
        
        # Step 2: Select room
        select_frame = ttk.LabelFrame(main_frame, text="Step 2: Select a Room", padding="15")
        select_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Room list
        columns = ("room_number", "type", "capacity", "location")
        self._room_tree = ttk.Treeview(
            select_frame,
            columns=columns,
            show="headings",
            height=6,
            selectmode="browse"
        )
        
        self._room_tree.heading("room_number", text="Room #")
        self._room_tree.heading("type", text="Type")
        self._room_tree.heading("capacity", text="Capacity")
        self._room_tree.heading("location", text="Location")
        
        self._room_tree.column("room_number", width=80)
        self._room_tree.column("type", width=150)
        self._room_tree.column("capacity", width=70)
        self._room_tree.column("location", width=150)
        
        room_scrollbar = ttk.Scrollbar(select_frame, orient=tk.VERTICAL, command=self._room_tree.yview)
        self._room_tree.configure(yscrollcommand=room_scrollbar.set)
        
        self._room_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        room_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self._room_tree.bind("<<TreeviewSelect>>", self._on_room_selected)
        
        # Room details label
        self._room_details_var = tk.StringVar(value="Select a room to see details")
        details_label = ttk.Label(select_frame, textvariable=self._room_details_var, 
                                   wraplength=400, justify=tk.LEFT)
        details_label.pack(fill=tk.X, pady=(10, 0))
        
        # Step 3: Confirm
        confirm_frame = ttk.Frame(main_frame)
        confirm_frame.pack(fill=tk.X, pady=(10, 0))
        
        self._reserve_btn = ttk.Button(
            confirm_frame,
            text="Confirm Reservation",
            command=self._on_confirm_reservation,
            width=25,
            state=tk.DISABLED
        )
        self._reserve_btn.pack(pady=10)
        
        # Status
        self._status_var = tk.StringVar(value="Enter search criteria and find rooms")
        status_label = ttk.Label(main_frame, textvariable=self._status_var, foreground="gray")
        status_label.pack(pady=(10, 0))
    
    def _on_find_rooms(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Search for available rooms based on criteria.
        """
        # Get values
        room_type = self._room_type_var.get()
        date_str = self._date_var.get().strip()
        start_str = self._start_var.get().strip()
        end_str = self._end_var.get().strip()
        group_size_str = self._group_var.get().strip()
        
        # Validate datetime range
        start_datetime_str = f"{date_str} {start_str}"
        end_datetime_str = f"{date_str} {end_str}"
        
        is_valid, error_msg, start_dt, end_dt = ValidationUtils.validate_datetime_range(
            start_datetime_str, end_datetime_str
        )
        
        if not is_valid:
            messagebox.showerror("Invalid Input", error_msg)
            return
        
        # Validate group size
        try:
            group_size = int(group_size_str)
            if group_size < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Input", "Group size must be a positive number")
            return
        
        # Validate capacity for room type
        is_valid_cap, error_cap = validate_capacity_for_room_type(group_size, room_type)
        if not is_valid_cap:
            messagebox.showerror("Invalid Group Size", error_cap)
            return
        
        # Create time slot
        try:
            self._current_time_slot = TimeSlot(start_dt, end_dt)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        self._current_group_size = group_size
        
        # Search rooms
        available_rooms = self._manager.search_available_rooms(
            room_type, self._current_time_slot, group_size
        )
        
        # Clear and populate tree
        for item in self._room_tree.get_children():
            self._room_tree.delete(item)
        
        self._available_rooms = available_rooms  # Store for selection
        
        if not available_rooms:
            self._status_var.set("No available rooms found")
            messagebox.showinfo("No Results", "No rooms available for the selected criteria")
            self._reserve_btn.config(state=tk.DISABLED)
        else:
            for room in available_rooms:
                self._room_tree.insert(
                    "",
                    tk.END,
                    values=(room.room_number, room.get_room_type(), room.capacity, room.location),
                    tags=(room.room_number,)
                )
            self._status_var.set(f"Found {len(available_rooms)} available room(s). Select one.")
    
    def _on_room_selected(self, event) -> None:
        """
        INSTANCE METHOD:
        ================
        Handle room selection from the tree.
        """
        selection = self._room_tree.selection()
        if not selection:
            return
        
        # Get selected item
        item = selection[0]
        values = self._room_tree.item(item, "values")
        room_number = values[0]
        
        # Find the room object
        for room in self._available_rooms:
            if room.room_number == room_number:
                self._selected_room = room
                break
        
        if self._selected_room:
            # Update details
            details = f"Selected: {self._selected_room.room_number}\n"
            details += f"Type: {self._selected_room.get_room_type()}\n"
            details += f"Capacity: {self._selected_room.capacity}\n"
            details += f"Location: {self._selected_room.location}\n"
            details += f"Rules: {self._selected_room.get_rules()}"
            self._room_details_var.set(details)
            
            # Enable reserve button
            self._reserve_btn.config(state=tk.NORMAL)
    
    def _on_confirm_reservation(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Confirm and create the reservation.
        """
        if not self._selected_room:
            messagebox.showerror("Error", "Please select a room first")
            return
        
        # Get purpose
        purpose = self._purpose_var.get().strip()
        
        # Confirm with user
        confirm_msg = (f"Confirm reservation?\n\n"
                      f"Room: {self._selected_room.room_number}\n"
                      f"Time: {self._current_time_slot}\n"
                      f"Group Size: {self._current_group_size}")
        
        if not messagebox.askyesno("Confirm Reservation", confirm_msg):
            return
        
        # Make reservation
        success, message, reservation = self._manager.make_reservation(
            self._current_user,
            self._selected_room,
            self._current_time_slot,
            self._current_group_size,
            purpose
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self._root.destroy()
        else:
            messagebox.showerror("Error", message)


# =============================================================================
# CLASS: ViewBookingsWindow
# =============================================================================
# Window for viewing user's reservations.
# =============================================================================
class ViewBookingsWindow:
    """
    Window for viewing all reservations made by the current user.
    """
    
    def __init__(self, root: tk.Toplevel, manager: ReservationManager, user: User):
        """
        CONSTRUCTOR:
        ============
        Initialize the view bookings window.
        """
        self._root = root
        self._manager = manager
        self._current_user = user
        
        self._root.title("My Bookings")
        self._root.geometry("800x500")
        self._root.resizable(True, True)
        
        self._create_widgets()
        self._load_bookings()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create the bookings display.
        """
        # Main frame
        main_frame = ttk.Frame(self._root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="My Reservations",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = ttk.Label(
            main_frame,
            text=f"Showing all active reservations for {self._current_user.name}",
            font=("Helvetica", 10),
            foreground="gray"
        )
        subtitle.pack(pady=(0, 15))
        
        # Treeview frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columns
        columns = ("res_id", "room", "type", "datetime", "duration", "group", "status")
        self._bookings_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=12
        )
        
        # Headings
        self._bookings_tree.heading("res_id", text="Reservation ID")
        self._bookings_tree.heading("room", text="Room")
        self._bookings_tree.heading("type", text="Type")
        self._bookings_tree.heading("datetime", text="Date & Time")
        self._bookings_tree.heading("duration", text="Duration")
        self._bookings_tree.heading("group", text="Group")
        self._bookings_tree.heading("status", text="Status")
        
        # Column widths
        self._bookings_tree.column("res_id", width=100)
        self._bookings_tree.column("room", width=80)
        self._bookings_tree.column("type", width=120)
        self._bookings_tree.column("datetime", width=150)
        self._bookings_tree.column("duration", width=70)
        self._bookings_tree.column("group", width=60)
        self._bookings_tree.column("status", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self._bookings_tree.yview)
        self._bookings_tree.configure(yscrollcommand=scrollbar.set)
        
        self._bookings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self._status_var = tk.StringVar(value="Loading...")
        status_label = ttk.Label(main_frame, textvariable=self._status_var)
        status_label.pack(pady=(10, 0))
        
        # Refresh button
        refresh_btn = ttk.Button(
            main_frame,
            text="Refresh",
            command=self._load_bookings,
            width=15
        )
        refresh_btn.pack(pady=(10, 0))
    
    def _load_bookings(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Load and display user's reservations.
        """
        # Clear existing
        for item in self._bookings_tree.get_children():
            self._bookings_tree.delete(item)
        
        # Get reservations
        reservations = self._manager.get_user_reservations(self._current_user)
        
        if not reservations:
            self._status_var.set("You have no active reservations")
        else:
            for res in reservations:
                duration = f"{res.time_slot.duration_minutes} min"
                self._bookings_tree.insert(
                    "",
                    tk.END,
                    values=(
                        res.reservation_id,
                        res.room.room_number,
                        res.room.get_room_type(),
                        str(res.time_slot),
                        duration,
                        res.group_size,
                        res.status.capitalize()
                    )
                )
            self._status_var.set(f"Found {len(reservations)} active reservation(s)")


# =============================================================================
# CLASS: CancelReservationWindow
# =============================================================================
# Window for cancelling reservations.
# =============================================================================
class CancelReservationWindow:
    """
    Window for cancelling existing reservations.
    """
    
    def __init__(self, root: tk.Toplevel, manager: ReservationManager, user: User):
        """
        CONSTRUCTOR:
        ============
        Initialize the cancel reservation window.
        """
        self._root = root
        self._manager = manager
        self._current_user = user
        
        self._root.title("Cancel Reservation")
        self._root.geometry("700x500")
        self._root.resizable(True, True)
        
        self._create_widgets()
        self._load_reservations()
    
    def _create_widgets(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Create the cancellation interface.
        """
        # Main frame
        main_frame = ttk.Frame(self._root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Cancel Reservation",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Instructions
        instr_label = ttk.Label(
            main_frame,
            text="Select a reservation from the list and click Cancel",
            font=("Helvetica", 10),
            foreground="gray"
        )
        instr_label.pack(pady=(0, 15))
        
        # Treeview frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columns
        columns = ("res_id", "room", "datetime", "group")
        self._res_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=10,
            selectmode="browse"
        )
        
        self._res_tree.heading("res_id", text="Reservation ID")
        self._res_tree.heading("room", text="Room")
        self._res_tree.heading("datetime", text="Date & Time")
        self._res_tree.heading("group", text="Group Size")
        
        self._res_tree.column("res_id", width=120)
        self._res_tree.column("room", width=100)
        self._res_tree.column("datetime", width=200)
        self._res_tree.column("group", width=80)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self._res_tree.yview)
        self._res_tree.configure(yscrollcommand=scrollbar.set)
        
        self._res_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection
        self._res_tree.bind("<<TreeviewSelect>>", self._on_selection)
        
        # Selected reservation info
        self._selected_info_var = tk.StringVar(value="No reservation selected")
        info_label = ttk.Label(main_frame, textvariable=self._selected_info_var, 
                               wraplength=500, justify=tk.LEFT)
        info_label.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(15, 0))
        
        # Cancel button
        self._cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel Selected Reservation",
            command=self._on_cancel,
            width=25,
            state=tk.DISABLED
        )
        self._cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_btn = ttk.Button(
            btn_frame,
            text="Refresh List",
            command=self._load_reservations,
            width=15
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Store selected reservation
        self._selected_reservation: Optional[Reservation] = None
    
    def _load_reservations(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Load user's active reservations.
        """
        # Clear
        for item in self._res_tree.get_children():
            self._res_tree.delete(item)
        
        # Get reservations
        reservations = self._manager.get_user_reservations(self._current_user)
        self._reservations = reservations  # Store for lookup
        
        if not reservations:
            self._selected_info_var.set("You have no active reservations to cancel")
            self._cancel_btn.config(state=tk.DISABLED)
        else:
            for res in reservations:
                self._res_tree.insert(
                    "",
                    tk.END,
                    values=(
                        res.reservation_id,
                        res.room.room_number,
                        str(res.time_slot),
                        res.group_size
                    ),
                    tags=(res.reservation_id,)
                )
            self._selected_info_var.set(f"Found {len(reservations)} reservation(s). Select one to cancel.")
    
    def _on_selection(self, event) -> None:
        """
        INSTANCE METHOD:
        ================
        Handle reservation selection.
        """
        selection = self._res_tree.selection()
        if not selection:
            return
        
        # Get selected item
        item = selection[0]
        values = self._res_tree.item(item, "values")
        res_id = values[0]
        
        # Find reservation
        for res in self._reservations:
            if res.reservation_id == res_id:
                self._selected_reservation = res
                break
        
        if self._selected_reservation:
            info = (f"Selected: {self._selected_reservation.reservation_id}\n"
                   f"Room: {self._selected_reservation.room.room_number} "
                   f"({self._selected_reservation.room.get_room_type()})\n"
                   f"Time: {self._selected_reservation.time_slot}\n"
                   f"Group Size: {self._selected_reservation.group_size}")
            self._selected_info_var.set(info)
            self._cancel_btn.config(state=tk.NORMAL)
    
    def _on_cancel(self) -> None:
        """
        INSTANCE METHOD:
        ================
        Handle cancel button click.
        """
        if not self._selected_reservation:
            messagebox.showerror("Error", "Please select a reservation first")
            return
        
        # Confirm
        confirm_msg = (f"Are you sure you want to cancel this reservation?\n\n"
                      f"Reservation ID: {self._selected_reservation.reservation_id}\n"
                      f"Room: {self._selected_reservation.room.room_number}\n"
                      f"Time: {self._selected_reservation.time_slot}")
        
        if not messagebox.askyesno("Confirm Cancellation", confirm_msg):
            return
        
        # Cancel
        success, message = self._manager.cancel_reservation(
            self._current_user,
            self._selected_reservation.reservation_id
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self._load_reservations()  # Refresh list
            self._cancel_btn.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", message)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
# This is where the application starts execution.
# =============================================================================
def main():
    """
    Main function to start the application.
    Creates the root window and initializes the login screen.
    """
    # Create the main tkinter window (root)
    root = tk.Tk()
    
    # Create the reservation manager (initializes sample data)
    manager = ReservationManager()
    
    # Create and show the login window
    login_window = LoginWindow(root, manager)
    
    # Start the tkinter event loop
    # This keeps the window open and responsive to user interactions
    root.mainloop()


# Standard Python entry point check
# This ensures main() only runs when the script is executed directly
if __name__ == "__main__":
    main()
