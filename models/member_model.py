class Member:
    def __init__(self, id, name, tel):
        self.id = id
        self.name = name
        self.tel = tel

    def __str__(self):
        return f"({self.id}) - {self.name} ({self.tel})"
    
    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["tel"] = self.tel

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["tel"])