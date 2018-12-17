from django.test import TestCase
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


texto = b"CristianRodrigu "
key = b"00112233445566778899aabbccddeeff"
iv = os.urandom(16)
aes_mode = AES.MODE_CBC
obj = AES.new(key, aes_mode, iv)
#Cifrado: 
# 1- El vector de inicialización iv entra al criptosistema con la clave K, esto nos resultará en un S1
# 2- Se operará S1 XOR texto[1]  resultará en el criptosistema 1 encriptado = C1
# 3- C1 vuelve a entrar al cipher con la clave y se obtiene un s2
# 4- Este s2 se vuelve a realizar una XOR con texto[2]
#El ciclo se repite hasta encriptar todo el mensaje. Es un cifrado en secuencia.
#Secuencia resultante = b'\x16\x18\xd9\xdcv6\x81\xf8$\xe8\xbd\x0e\x15\x1cKB'
ciphertext = obj.encrypt(texto)
print(ciphertext)

#Descifrado:
# A partir de los bloques obtenidos del cifrado operaremos de la siguiente manera
# 1- iv (vector de inicialización) con la clave k entran al criptosistema => S1
# 2- S1 XOR c1(bloque cifrado) = mensaje en claro
# 3- C1 con k entran al criptosistema => S2
# 4- S2 XOR c2 = mensaje en claro 
cipher = AES.new(key, aes_mode, iv)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)    