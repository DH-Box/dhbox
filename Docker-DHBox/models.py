from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask import Flask

db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))



# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=False)
#     email = Column(String(120), unique=False)
#     ip = Column(String(50), unique=False)
#     active = Column(Boolean(), unique=False)

#     # def get_id(self):
#     #     try:
#     #         return unicode(self.id)  # python 2
#     #     except NameError:
#     #         return str(self.id)  # python 3

#     # def is_active(self):
#     #     # Need to define 'active'
#     #     return True

#     # def is_anonymous(self):
#     #     return False

#     # def is_authenticated(self):
#     #     return True

#     def __init__(self, name=None, email=None, ip=None):
#         self.name = name
#         self.email = email
#         self.ip = ip

#     def __repr__(self):
#         return '<User %r>' % (self.name)