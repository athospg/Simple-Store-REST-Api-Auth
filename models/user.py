from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    # Columns in the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
