from part3.app.models import BaseModel

from sqlalchemy import Column, String


class Amenity(BaseModel):
    __tablename__ = "amenities"
    name = Column(String(50), nullable=False)

    def __init__(self, name: str):
        super().__init__()
        if not isinstance(name, str) or not len(name) < 50:
            raise ValueError("Name is required and must be 50 characters or fewer")
        self.name = name
        # Amenity.amenities_set.add(self)
