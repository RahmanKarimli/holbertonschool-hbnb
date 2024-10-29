import re

from app.models import BaseModel


class User(BaseModel):
    users_set = set()

    def __init__(self, first_name: str, last_name: str, email: str, is_admin=False):
        super().__init__()
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not isinstance(first_name, str) or not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or fewer")
        if not isinstance(last_name, str) or not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or fewer")
        if not valid:
            raise ValueError("Invalid email")
        if email in User.users_set:
            raise ValueError("Email already registered")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        User.users_set.add(email)
        User.users_set.add(self)

    def add_place(self, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")
        self.places.append(place)
