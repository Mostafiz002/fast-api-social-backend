from pwdlib import PasswordHash

password_context = PasswordHash.recommended()

def hash_password(password: str):
    return password_context.hash(password)