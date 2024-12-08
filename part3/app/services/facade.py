from part3.app.models.amenity import Amenity
from part3.app.models.place import Place
from part3.app.models.review import Review
from part3.app.models.user import User
from part3.app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User
    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["email"],
                    password=user_data["password"], is_admin=user_data.get("is_admin"))
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)

        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.user_repo.update(user_id, user)
        return user

    # Amenity
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)

        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # Places
    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        title = place_data['title']
        description = place_data['description']
        price = place_data['price']
        latitude = place_data['latitude']
        longitude = place_data['longitude']
        owner_id = place_data['owner_id']
        amenities = place_data.get('amenities', [])
        reviews = place_data.get('reviews', [])

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        place = Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude,
                      owner=owner)

        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)
        for review_id in reviews:
            review = self.review_repo.get(review_id)
            if review:
                place.add_review(review)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)
        amenities = place_data.get('amenities', [])
        reviews = place_data.get('reviews', [])

        place.amenities = []  # Clear existing amenities
        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            place.add_amenity(amenity)
        place.reviews = []  # Clear existing reviews
        for review_id in reviews:
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError("Review not found")
            place.add_review(review_id)

        self.place_repo.update(place_id, place)
        return place

    # Reviews
    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        text = review_data['text']
        rating = review_data['rating']
        user_id = review_data['user_id']
        place_id = review_data['place_id']

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(text=text, rating=rating, user=user, place=place)

        self.review_repo.add(review)
        place.add_review(review)
        self.place_repo.update(place.id, place)

        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.get_reviews()

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)

        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        review = self.review_repo.get(review_id)
        if not review:
            return False
        place = review.place

        if place and review in place.reviews:
            place.reviews.remove(review)
            self.place_repo.update(place.id, place)
        self.review_repo.delete(review_id)
        return True
