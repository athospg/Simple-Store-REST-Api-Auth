from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    # Columns in the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))