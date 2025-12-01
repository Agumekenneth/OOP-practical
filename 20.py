"""
OOP Exam Solutions — 20 Questions (each worth 20 marks)
Author: Student-friendly implementation
Run this file to see demo outputs for each question.

Each section:
 - shows the class(es)
 - demonstrates correct OOP usage (encapsulation, validation, inheritance, polymorphism, composition)
 - includes a small demo that prints results
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
import re
import csv
from typing import List, Optional


# ----------------------------
# Q1: Library Book Borrowing System
# ----------------------------
class BorrowRecord:
    """Record a single borrowing event."""
    def __init__(self, title: str, borrower: str, date_borrowed: Optional[datetime] = None):
        if not title.strip():
            raise ValueError("Book title cannot be empty.")
        self._title = title.strip()
        self._borrower = borrower.strip()
        self._date = date_borrowed or datetime.now()
        self._returned = False

    def mark_returned(self):
        self._returned = True

    def is_returned(self) -> bool:
        return self._returned

    def get_date(self) -> datetime:
        return self._date

    def __str__(self):
        status = "Returned" if self._returned else "Borrowed"
        return f"{self._title} by {self._borrower} on {self._date.date()} [{status}]"


class Library:
    """Manage borrow records and summary."""
    def __init__(self):
        self._records: List[BorrowRecord] = []

    def borrow_book(self, title: str, borrower: str):
        r = BorrowRecord(title, borrower)
        self._records.append(r)
        return r

    def borrowed_today_count(self) -> int:
        today = datetime.now().date()
        return sum(1 for r in self._records if r.get_date().date() == today)

    def list_records(self) -> List[BorrowRecord]:
        return list(self._records)


# ----------------------------
# Q2: Mobile Money Wallet
# ----------------------------
class MobileWallet:
    """Secure wallet: balance is private; use deposit/withdraw only."""
    def __init__(self, customer_name: str, initial_balance: float = 0.0):
        self._name = customer_name
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.__balance = float(initial_balance)  # private __ to prevent direct external modification

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount
        return self.__balance

    def get_balance_safe(self) -> float:
        """Controlled read (no direct write)."""
        return float(self.__balance)

    def __str__(self):
        return f"{self._name} Wallet (balance hidden)"


# ----------------------------
# Q3: Bus Ticket Reservation System
# ----------------------------
class TicketGenerator:
    _counter = 0

    @classmethod
    def next_ticket(cls) -> str:
        cls._counter += 1
        return f"TK{cls._counter:05d}"


class BusTicket:
    def __init__(self, passenger_name: str, destination: str):
        self._passenger = passenger_name.strip()
        self._destination = destination.strip()
        self._ticket_no = TicketGenerator.next_ticket()

    def display_ticket(self) -> str:
        return f"Ticket {self._ticket_no} | Passenger: {self._passenger} | Destination: {self._destination}"


# ----------------------------
# Q4: Employee Payroll Management
# ----------------------------
class Employee:
    def __init__(self, name: str, position: str, salary: float):
        self._name = name.strip()
        self._position = position.strip()
        self._salary = float(0)
        self.set_salary(salary)

    def set_salary(self, amount: float):
        if amount < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = float(amount)

    def get_salary(self) -> float:
        return float(self._salary)

    def deduct_tax(self):
        """Deduct 30% tax from salary."""
        self._salary = self._salary * 0.70

    def __str__(self):
        return f"{self._name} ({self._position}) - Salary: UGX {self._salary:,.2f}"


# ----------------------------
# Q5: Movie Theatre Seat Booking
# ----------------------------
class SeatBooking:
    def __init__(self, movie_name: str):
        self._movie = movie_name
        self._bookings = {}  # seat_no -> customer name

    def book_seat(self, seat_no: str, customer: str) -> bool:
        if seat_no in self._bookings:
            return False
        self._bookings[seat_no] = customer
        return True

    def is_booked(self, seat_no: str) -> bool:
        return seat_no in self._bookings

    def print_receipt(self, seat_no: str) -> str:
        if seat_no not in self._bookings:
            return "Seat not booked."
        cust = self._bookings[seat_no]
        return f"Movie: {self._movie}\nSeat: {seat_no}\nCustomer: {cust}"


# ----------------------------
# Q6: Bank Loan Processing System
# ----------------------------
class Loan:
    def __init__(self, customer: str, loan_amount: float, annual_interest_rate: float, years: int = 1):
        self._customer = customer
        if loan_amount <= 0:
            raise ValueError("Loan amount must be positive.")
        if not (0 <= annual_interest_rate <= 100):
            raise ValueError("Interest rate must be between 0 and 100 percent.")
        if years <= 0:
            raise ValueError("Years must be positive.")
        self._amount = float(loan_amount)
        self._rate = float(annual_interest_rate) / 100.0
        self._years = int(years)

    def calculate_monthly_payment(self) -> float:
        """Return monthly payment using amortization formula."""
        n = self._years * 12
        r = self._rate / 12
        if r == 0:
            return self._amount / n
        payment = (self._amount * r) / (1 - (1 + r) ** (-n))
        return float(payment)


# ----------------------------
# Q7: Hospital Patient Registration
# ----------------------------
class Patient:
    def __init__(self, name: str, age: int, condition: str):
        self._name = name.strip()
        self.set_age(age)
        self._condition = condition.strip()

    def set_age(self, age: int):
        if not (0 <= age <= 120):
            raise ValueError("Age must be between 0 and 120.")
        self._age = int(age)

    def summary(self) -> str:
        return f"Patient: {self._name}, Age: {self._age}, Condition: {self._condition}"


# ----------------------------
# Q8: Online Shop Product Inventory
# ----------------------------
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self._name = name.strip()
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._price = float(price)
        self._quantity = int(quantity)

    def add_stock(self, qty: int):
        if qty < 0:
            raise ValueError("Cannot add negative stock.")
        self._quantity += int(qty)

    def reduce_stock(self, qty: int):
        if qty < 0:
            raise ValueError("Cannot reduce by negative stock.")
        if qty > self._quantity:
            raise ValueError("Not enough stock.")
        self._quantity -= int(qty)

    def report(self) -> str:
        return f"{self._name} | Price: UGX {self._price:,.2f} | Quantity: {self._quantity}"


class Inventory:
    def __init__(self):
        self._items: List[Product] = []

    def add_product(self, product: Product):
        self._items.append(product)

    def inventory_report(self) -> str:
        lines = [p.report() for p in self._items]
        return "\n".join(lines)


# ----------------------------
# Q9: Lecturer Course Allocation
# ----------------------------
class Lecturer:
    def __init__(self, name: str, staff_id: str):
        self._name = name.strip()
        self._staff_id = staff_id.strip()
        self._courses: List[str] = []

    def assign_course(self, course: str):
        if course.strip() not in self._courses:
            self._courses.append(course.strip())

    def get_courses(self) -> List[str]:
        return list(self._courses)

    def __str__(self):
        courses = ", ".join(self._courses) or "None"
        return f"{self._name} ({self._staff_id}) | Courses: {courses}"


# ----------------------------
# Q10: Electricity Billing System
# ----------------------------
class ElectricityBill:
    def __init__(self, customer: str, units_consumed: float, cost_per_unit: float):
        self._customer = customer.strip()
        if units_consumed < 0:
            raise ValueError("Units consumed cannot be negative.")
        if cost_per_unit < 0:
            raise ValueError("Cost per unit cannot be negative.")
        self._units = float(units_consumed)
        self._cost = float(cost_per_unit)

    def calculate_bill(self) -> float:
        return self._units * self._cost


# ----------------------------
# Q11: Hotel Room Booking using Inheritance
# ----------------------------
class Room:
    def __init__(self, room_number: str, base_price: float):
        self._room_number = room_number
        self._base_price = float(base_price)

    def calculate_total(self) -> float:
        return self._base_price


class StandardRoom(Room):
    def calculate_total(self) -> float:
        return super().calculate_total()  # no extras


class DeluxeRoom(Room):
    def __init__(self, room_number: str, base_price: float, extra_charge: float):
        super().__init__(room_number, base_price)
        self._extra = float(extra_charge)

    def calculate_total(self) -> float:
        return self._base_price + self._extra


# ----------------------------
# Q12: Car Rental Management
# ----------------------------
class CarRental:
    def __init__(self, customer: str, car_model: str, days_rented: int, daily_rate: float):
        self._customer = customer
        self._car_model = car_model
        if days_rented <= 0:
            raise ValueError("Days must be greater than 0.")
        self._days = int(days_rented)
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")
        self._daily_rate = float(daily_rate)

    def compute_cost(self) -> float:
        return self._days * self._daily_rate


# ----------------------------
# Q13: Online Quiz Grading System
# ----------------------------
class QuizResult:
    def __init__(self, student: str, score: float, total: float):
        self._student = student
        if score < 0 or total <= 0:
            raise ValueError("Score and total must be positive.")
        if score > total:
            raise ValueError("Score cannot exceed total marks.")
        self._score = float(score)
        self._total = float(total)

    def grade(self) -> str:
        pct = (self._score / self._total) * 100
        if pct >= 85:
            return "A"
        if pct >= 70:
            return "B"
        if pct >= 55:
            return "C"
        if pct >= 40:
            return "D"
        return "F"


# ----------------------------
# Q14: Gym Membership System
# ----------------------------
class Member:
    def __init__(self, name: str, membership_type: str, monthly_fee: float):
        if not re.match(r"^[A-Za-z ]+$", name.strip()):
            raise ValueError("Name must contain only letters and spaces.")
        if monthly_fee < 0:
            raise ValueError("Monthly fee cannot be negative.")
        self._name = name.strip()
        self._membership_type = membership_type.strip()
        self._monthly_fee = float(monthly_fee)

    def summary(self) -> str:
        return f"Member: {self._name} | Type: {self._membership_type} | Fee: UGX {self._monthly_fee:,.2f}"


# ----------------------------
# Q15: Animal Registration System
# ----------------------------
class Animal:
    def __init__(self, name: str, species: str, age: float):
        if age <= 0:
            raise ValueError("Age must be greater than 0.")
        self._name = name.strip()
        self._species = species.strip()
        self._age = float(age)

    def describe(self) -> str:
        return f"{self._name} ({self._species}) - Age: {self._age}"


# ----------------------------
# Q16: Campus Parking System
# ----------------------------
class ParkingRecord:
    PLATE_PATTERN = re.compile(r"^[A-Z]{1,3}-\d{1,4}$")  # e.g., ABC-1234 or A-12

    def __init__(self, plate: str, owner: str, entry_time: Optional[datetime] = None):
        if not ParkingRecord.PLATE_PATTERN.match(plate.strip().upper()):
            raise ValueError("Plate number must match pattern LETTERS-DIGITS (e.g., ABC-1234).")
        self._plate = plate.strip().upper()
        self._owner = owner.strip()
        self._entry = entry_time or datetime.now()
        self._exit: Optional[datetime] = None

    def exit_parking(self, exit_time: Optional[datetime] = None):
        self._exit = exit_time or datetime.now()

    def compute_duration(self) -> Optional[timedelta]:
        if self._exit is None:
            return None
        return self._exit - self._entry


# ----------------------------
# Q17: SMS Notification System
# ----------------------------
class SMS:
    MAX_LEN = 160

    def __init__(self, sender: str, receiver: str, text: str):
        if len(text) > SMS.MAX_LEN:
            raise ValueError("Message exceeds 160 characters.")
        self._sender = sender
        self._receiver = receiver
        self._text = text

    def send(self) -> str:
        # Simulation: print confirmation
        return f"Sent from {self._sender} to {self._receiver}: {self._text[:30]}..."


# ----------------------------
# Q18: Music Playlist Manager
# ----------------------------
@dataclass(eq=True, frozen=True)
class Song:
    title: str
    artist: str
    duration_seconds: int


class Playlist:
    def __init__(self):
        self._songs: List[Song] = []

    def add_song(self, song: Song):
        if song in self._songs:
            return False
        self._songs.append(song)
        return True

    def show_playlist(self) -> str:
        lines = []
        for i, s in enumerate(self._songs, start=1):
            mins = s.duration_seconds // 60
            secs = s.duration_seconds % 60
            lines.append(f"{i}. {s.title} - {s.artist} ({mins}:{secs:02d})")
        return "\n".join(lines)


# ----------------------------
# Q19: University Research Project Tracking
# ----------------------------
class ResearchProject:
    def __init__(self, title: str, supervisor: str, progress_percent: float = 0.0):
        if not (0 <= progress_percent <= 100):
            raise ValueError("Progress must be between 0 and 100.")
        self._title = title.strip()
        self._supervisor = supervisor.strip()
        self._progress = float(progress_percent)

    def update_progress(self, increment: float):
        if increment < 0:
            raise ValueError("Increment must be non-negative.")
        self._progress = min(100.0, self._progress + increment)

    def get_progress(self) -> float:
        return self._progress


# ----------------------------
# Q20: Taxi Fare Calculator
# ----------------------------
class TaxiFare:
    def __init__(self, passenger: str, distance_km: float, cost_per_km: float):
        if distance_km <= 0:
            raise ValueError("Distance must be positive.")
        if cost_per_km < 0:
            raise ValueError("Cost per km cannot be negative.")
        self._passenger = passenger
        self._distance = float(distance_km)
        self._cost_per_km = float(cost_per_km)

    def compute_fare(self) -> float:
        return round(self._distance * self._cost_per_km, 2)


# ----------------------------
# Demo usage for each question
# ----------------------------
if __name__ == "__main__":
    print("=== Q1 Library Demo ===")
    lib = Library()
    lib.borrow_book("Data Structures", "Alice")
    lib.borrow_book("Intro to Python", "Bob")
    print("Records:", [str(r) for r in lib.list_records()])
    print("Borrowed today:", lib.borrowed_today_count())

    print("\n=== Q2 Mobile Wallet Demo ===")
    wallet = MobileWallet("Maria", 1000.0)
    print(wallet)
    wallet.deposit(500)
    try:
        wallet.withdraw(2000)  # will fail
    except ValueError as e:
        print("Failed transaction (expected):", e)
    print("Safe balance read:", wallet.get_balance_safe())

    print("\n=== Q3 Bus Ticket Demo ===")
    t1 = BusTicket("John Doe", "Kitgum")
    t2 = BusTicket("Jane Roe", "Mbale")
    print(t1.display_ticket())
    print(t2.display_ticket())

    print("\n=== Q4 Employee Payroll Demo ===")
    emp = Employee("Mark", "Developer", 1000000)
    print(emp)
    emp.deduct_tax()
    print("After tax:", emp.get_salary())

    print("\n=== Q5 Seat Booking Demo ===")
    theater = SeatBooking("Avengers")
    print("Book A1:", theater.book_seat("A1", "Sam"))
    print("Book A1 again:", theater.book_seat("A1", "Zoe"))
    print(theater.print_receipt("A1"))

    print("\n=== Q6 Loan Demo ===")
    loan = Loan("Eve", 1_000_000, 12.0, years=2)
    print("Monthly payment:", round(loan.calculate_monthly_payment(), 2))

    print("\n=== Q7 Patient Demo ===")
    p = Patient("Anne", 30, "Cough")
    print(p.summary())

    print("\n=== Q8 Inventory Demo ===")
    prod1 = Product("Soap", 2500, 10)
    prod2 = Product("Shampoo", 6000, 5)
    inv = Inventory()
    inv.add_product(prod1)
    inv.add_product(prod2)
    prod1.reduce_stock(2)
    prod2.add_stock(3)
    print(inv.inventory_report())

    print("\n=== Q9 Lecturer Demo ===")
    lect = Lecturer("Dr. Kato", "ST123")
    lect.assign_course("Algorithms")
    lect.assign_course("Databases")
    lect.assign_course("Databases")  # duplicate ignored
    print(lect)

    print("\n=== Q10 Electricity Bill Demo ===")
    bill = ElectricityBill("Moses", 350, 650)
    print("Total bill:", bill.calculate_bill())

    print("\n=== Q11 Rooms Demo ===")
    sr = StandardRoom("101", 100_000)
    dr = DeluxeRoom("201", 120_000, 30_000)
    print("Standard total:", sr.calculate_total())
    print("Deluxe total:", dr.calculate_total())

    print("\n=== Q12 Car Rental Demo ===")
    rent = CarRental("Peter", "Toyota", 3, 50_000)
    print("Cost:", rent.compute_cost())

    print("\n=== Q13 Quiz Demo ===")
    q = QuizResult("Sam", 42, 50)
    print("Grade:", q.grade())

    print("\n=== Q14 Gym Demo ===")
    mem = Member("Grace Mukasa", "Premium", 120000)
    print(mem.summary())

    print("\n=== Q15 Animal Demo ===")
    a = Animal("Simba", "Lion", 3)
    print(a.describe())

    print("\n=== Q16 Parking Demo ===")
    rec = ParkingRecord("UG-123", "Owner A")
    rec.exit_parking(rec._entry + timedelta(hours=2, minutes=30))
    print("Duration (hrs):", rec.compute_duration())

    print("\n=== Q17 SMS Demo ===")
    sms = SMS("Alice", "Bob", "Hello Bob! This is a test message.")
    print(sms.send())

    print("\n=== Q18 Playlist Demo ===")
    pl = Playlist()
    s1 = Song("Song A", "Artist 1", 210)
    s2 = Song("Song B", "Artist 2", 180)
    pl.add_song(s1)
    pl.add_song(s2)
    pl.add_song(s1)  # duplicate ignored
    print(pl.show_playlist())

    print("\n=== Q19 Research Demo ===")
    proj = ResearchProject("AI Thesis", "Dr. O", 20.0)
    proj.update_progress(30)
    print("Progress:", proj.get_progress())

    print("\n=== Q20 Taxi Fare Demo ===")
    fare = TaxiFare("Alice", 12.5, 450.0)
    print("Fare:", fare.compute_fare())

    print("\n=== End of Demos ===")
