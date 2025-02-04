#Хеширование пароля
import hashlib
def hash_password(password: str, author_login: str):
    password += password[0] + password[-1] + 'some_salt_for_hashing' + author_login
    password = hashlib.sha256(password.encode()).hexdigest()
    return password