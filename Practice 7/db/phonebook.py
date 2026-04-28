class PhoneBook:
    def __init__(self, id: int, first_name: str, last_name: str, phone: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __repr__(self):  # toString
        return f"{self.id} {self.first_name} {self.last_name} {self.phone}"
