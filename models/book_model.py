class Book:
    def __init__(self, id, title, author, state, year_published):
        self.id = id
        self.title = title
        self.author = author
        self.state = state
        self.year_published = year_published

    def __str__(self):
        return f"({self.id}) - {self.title} by {self.author} published in {self.year_published}. State: {self.state}"
    
    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["title"] = self.title
        result["author"] = self.author
        result["state"] = self.state
        result["year_published"] = self.year_published

        return result

    @classmethod
    def from_dict(clc, data):
        return clc(data["id"], data["title"], data["author"], data["state"], data["year_published"])