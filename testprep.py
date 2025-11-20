class BorrowRecord:
    def __init__(self, title, borrowerName, dateBorrowed, status):
        self.title = title
        self._borrowerName = borrowerName
        self._dateBorrowed = dateBorrowed
        self._status = status
    
    # title Validation
    def _set_title(self,title):
        if title.strip() =="":
            raise ValueError("Title cannot be empty")
        self.title = title

    # Getters(Encapsulation)
    def get_title(self):
        return self.title
    def get_borrowerName(self):
        return self._borrowerName
    def get_dateBorrowed(self):
        return self._dateBorrowed
    def get_status(self):
        return self._status
    
    # Mark as returned (behavior)
    def marked_returned(self):
        self._status ="Returned"
    
    