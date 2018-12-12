"""
from Crypto.Cipher import DES
import os

iv = os.urandom(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_OFB)
plaintext = b'sona si latine loqueris '
msg = cipher.iv + cipher.encrypt(plaintext) #iv hace referencia al vector de inicialización del algoritmo DES

print(msg)
"""
#pip3 install pycryptodome añadir al requirements
from Crypto.Cipher import AES 
import binascii,os

texto = "CristianRodrigu "
key = "00112233445566778899aabbccddeeff"
iv = os.urandom(16)
aes_mode = AES.MODE_CBC
obj = AES.new(key, aes_mode, iv)
ciphertext = obj.encrypt(texto)

print(ciphertext)

cipher = AES.new(key, aes_mode, iv)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)    