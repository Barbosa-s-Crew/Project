import hashlib
import os

salt = os.urandom(32)


def encrypt(password):
	key = hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		b'salt',
		100000,
	)
	newStorage = salt + key
	return newStorage
	#salt = storage[:32]
	#key = storage[32:]


def verify(password, oldStorage):
	oldSalt = oldStorage[:32]
	print(oldSalt)
	key = hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		b'oldSalt',
		100000,
	)
	newStorage = oldSalt + str(key)
	return newStorage
	#salt = storage[:32]
	#key = storage[32:]

print(encrypt("thomaspassword"))
