class BorrowRecord:
    def __init__(self, title, borrowerName, dateBorrowed, status):
        self.title = title
        self._borrowerName = borrowerName
        self._dateBorrowed = dateBorrowed
        self._status = status
        books =[]
