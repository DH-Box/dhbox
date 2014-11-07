from database import db_session
from models import User
import emailing
import sys


def check_for_preexisting_dhbox(email):
    already_has_dhbox_check = User.query.filter(User.email == email).first()
    return already_has_dhbox_check

def add_dhbox_user_to_db(email, name, ip_address):
    u = User(name, email, ip_address)
    db_session.add(u)
    db_session.commit()

if __name__ == '__main__':
    add_dhbox_user_to_db(sys.argv[1], sys.argv[2], sys.argv[3])