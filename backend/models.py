from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    ip = Column(String(50), unique=True)

    def __init__(self, name=None, email=None, ip=None):
        self.name = name
        self.email = email
        self.ip = ip

    def __repr__(self):
        return '<User %r>' % (self.name)