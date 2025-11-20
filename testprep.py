class BorrowRecord:
    def __init__(self, title, borrowerName, dateBorrowed, status):
        self.title = title
        self._borrowerName = borrowerName
        self._dateBorrowed = dateBorrowed
        self._status = status
        self.copies = {}
    def _set_title(self,title):
        if title.strip() =="":
            raise ValueError("Title cannot be empty")
        self.title = title

    
    
