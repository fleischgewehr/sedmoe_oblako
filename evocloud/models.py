from flask_login import UserMixin

from evocloud import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)

    def __repr__(self):
        return 'User({0}, {1})'.format(self.username, self.email)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(50), nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    hash = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return 'File({0}, {1})'.format(self.file, self.hash)

