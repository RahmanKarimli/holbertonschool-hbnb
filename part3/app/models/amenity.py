from sqlalchemy.orm import relationship

from part3.app.models import BaseModel
from part3.app import db

from sqlalchemy import Column, String, ForeignKey

place_amenity_association = db.Table("place_amenity_association",
    Column("place_id", String(36), ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", String(36), ForeignKey("amenities.id", primary_key=True))
)

class Amenity(BaseModel):
    __tablename__ = "amenities"
    name = Column(String(50), nullable=False)

    places = relationship("Place", secondary=place_amenity_association, back_populates="amenities")

    def __init__(self, name: str):
        super().__init__()
        if not isinstance(name, str) or not len(name) < 50:
            raise ValueError("Name is required and must be 50 characters or fewer")
        self.name = name
