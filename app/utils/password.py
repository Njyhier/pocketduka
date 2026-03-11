from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

async def get_password_hash(password: str):
  return password_hash.hash(password)

async def verify_password(plain_password: str, hashed_password: str):
  return password_hash.verify(plain_password, hashed_password)
