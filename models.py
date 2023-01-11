"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

GENERIC_IMAGE = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# class User(db.Model):
#     """Site user."""

#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.Text, nullable=False)
#     last_name = db.Column(db.Text, nullable=False)
#     image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

#     @property
#     def full_name(self):
#         """Return full name of user."""

#         return f"{self.first_name} {self.last_name}"

class Pet(db.Model):
    """Adoptable pet."""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def image_url(self):
        """Return image for pet -- bespoke or generic."""

        return self.photo_url or GENERIC_IMAGE

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
