from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    # Columns in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name
