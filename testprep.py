from datetime import date

class BorrowRecord:
    def __init__(self, title, borrowerName, dateBorrowed, status):
        self._set_title(title)              
        self._borrowerName = borrowerName
        self._dateBorrowed = dateBorrowed
        self._status = status
    
    # title Validation
    def _set_title(self, title):
        if title.strip() == "":
            raise ValueError("Title cannot be empty")
        self._title = title

    # Getters 
    def get_title(self):
        return self._title
    def get_borrowerName(self):
        return self._borrowerName
    def get_dateBorrowed(self):
        return self._dateBorrowed
    def get_status(self):
        return self._status
    
    # Mark as returned
    def marked_returned(self):
        self._status = "Returned"

class Library:
    def __init__(self):
        self._records = [] 

    def add_record(self, record):
        self._records.append(record)

    # print summary 
    def print_summary(self):
        today = date.today().isoformat()
        today_count = sum(1 for r in self._records if r.get_dateBorrowed() == today)
        print(f"Total books borrowed today: {today_count}")

library = Library()

record1 = BorrowRecord("Data Science 101", "Kenneth", date.today().isoformat(), "Borrowed")
record2 = BorrowRecord("Python Programming", "Lydia", date.today().isoformat(), "Borrowed")

library.add_record(record1)
library.add_record(record2)

library.print_summary()
