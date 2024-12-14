import re

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from part3.app.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    # If users have related "places", define the relationship here (update accordingly):
    places = relationship('Place', backref='owner', lazy=True)

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin=False):
        super().__init__()
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not isinstance(first_name, str) or not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or fewer")
        if not isinstance(last_name, str) or not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or fewer")
        if not valid:
            raise ValueError("Invalid email")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password: str):
        from part3.app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        from part3.app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
