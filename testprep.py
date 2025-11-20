from datetime import date
class BorrowRecord:
    def __init__(self, title, borrowerName, dateBorrowed, status):
        self._set_title(title)              
        self._borrowerName = borrowerName
        self._dateBorrowed = dateBorrowed
        self._status = status
    
    # title Validation (abstraction)
    def _set_title(self, title):
        if title.strip() == "":
            raise ValueError("Title cannot be empty")
        self._title = title

    # Getters (encapsulation + abstraction)
    def get_title(self):
        return self._title
    def get_borrowerName(self):
        return self._borrowerName
    def get_dateBorrowed(self):
        return self._dateBorrowed
    def get_status(self):
        return self._status
    
    # Mark as returned (behavior)
    def marked_returned(self):
        self._status = "Returned"
class Library:
    def __init__(self):
        self._records = [] # holds BorrowRecord objects
    def add_record(self, record):
        self._records.append(record)

    # print summary 
    def print_summary(self):
        today = date.today().isoformat()
        today_count = sum(1 for r in self.records if r.get_date() == today)