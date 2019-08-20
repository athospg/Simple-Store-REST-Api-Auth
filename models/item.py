from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    # Columns in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))