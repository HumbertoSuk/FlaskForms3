from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password, usertype, fullname=None):
        self.id = id
        self.username = username
        self.password = password
        self.usertype = usertype
        self.fullname = fullname
