from passlib.hash import pbkdf2_sha265

def hash_password(password):

    return pbkdf2_sha265.hash(password)

def check_password(password, hashed):
    return pbkdf2_sha265.verify(password, hashed)
    