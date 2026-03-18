class Loan:
    def __init__(self, id, member_id, book_id, date, return_date, is_returned):
        self.id = id
        self.member_id = member_id
        self.book_id = book_id
        self.date = date
        self.return_date = return_date
        self.is_returned = is_returned

    def __str__(self):
        return f"({self.id}) - Member ID: {self.member_id}, Book ID: {self.book_id}, rented on: {self.date}, to return before {self.return_date}"
    
    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["member_id"] = self.member_id
        result["book_id"] = self.book_id
        result["date"] = self.date
        result["return_date"] = self.return_date
        result["is_returned"] = self.is_returned
        return result
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["member_id"], data["book_id"], data["date"], data["return_date"], data["is_returned"])