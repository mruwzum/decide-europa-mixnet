
"""
La autoridad Bob elige los siguientes 4 parámetros:
    - Un primo P largo de tal forma que la descomposición de ese primo sea intratable.
    - Saca también un parámetro de seguridad T, de tal forma que P >= 2^t. Normalmente con t = 40 es una seguridad adecuada.
    - Bob establece una firma segura con un algortimo secreto de firma que es Firma(Bob) y un algoritmo de verificaión SHA2.
    - Una función segura de Hash para hashear el mensaje antes de firmarlo.

Entrega el mensaje a alicia:
    - Bob establece la identidad de Alice como el certificado de nacimiento o el pasaporte, y crea un String IDAlice.
    - Alicia elige un exponente random A. De tal forma que 0<=A<=P-2.
    - Alicia calcula V que es congrunte con el generador V=ALFA-A mod P.
    - Devuelve V a Bob.
    - Bob genera una firma (S = IDAlice, V). Y le da el certificado que es Cert=(IDAlice, V, S).

Acciones:
    - Alica elige un número random R en el mismo rango que A, y prueba que el máximo común divisor(R, P-1) = 1. Que es lo mismo que X congruente con A^R mod P.
    - Alice devuelve el certificado que ella crea CertAlice = (IDAlice, V, S).
    - Alice manda X a Bob.
    - Bob verifica la firma de Alice y envia TRUE si lo es. Además, elige un número random E en el rango 1 < E < 2. Y se lo manda a Alice.
    - Alicia calcula Y congruente con A*E+R mod P-1.
    - Alicia envía Y a Bob.
    - Bob calcula Z congruente con ALFA^Y * V^E mod P.
    - Bob acepta que es verdadero si Z = X.
"""

# To get a different random number everytime
import time
from numpy import mod
import numpy as np
import sympy
import random
from math import gcd
primePrime = sympy.randprime(0, 9999999999)
semilla = int(round(time.time() * primePrime))

# Generator for random number generation
def generador_módulo_aleatorio(k, módulo):
	num = 0
	granPrimo = sympy.randprime(0, 1000000)
	while(num < k):
		a = mod(granPrimo, módulo)
		while(gcd(a, módulo) != 1):
			a = mod(granPrimo, módulo)
		yield a
		num += 1

def generador_módulo_aleatorio_mio():
	num = 0
	while(num < k):
		a = np.int64(num)
		yield a
		num += 1


class testSetUp:
	#Inicialización de las variables que se van a utilizar a lo largo de la
	#ejecución de las pruebas de cero conocimiento.
	def __init__(self, modbits, k, semilla,p,g):
		self.k = k
		granPrimo = sympy.randprime(0, 1000000)
		random.seed(semilla)
		random.getstate()
		self.p = sympy.prime(2^modbits + granPrimo)
		#print("p : ", self.p)
		self.q = sympy.nextprime(2^modbits + granPrimo)
		#print("q : ", self.q)
		#if self.p == self.q:
			#print("Los primos son iguales. Por favor, ejecútalo de nuevo.")
		self.n = self.p*self.q
		#print("n = "+str(self.n))
		self.a = list(generador_módulo_aleatorio(k, self.n))
		assert sum([gcd(i, self.n) for i in self.a]) == len(self.a)
		self.asq = [i**(2, self.n) for i in self.a]
		#print(asq)
		
#Parte del algoritmo que se encarga de verificar la integridad de las claves	
class Alice:
	sk = np.array([173,33],dtype=np.int64)
	def __init__(self, n, p, g):
		self.n = n
		#self.sk = sk
		nuestrak = np.array([p,g],dtype=np.int64)
		self.sk = nuestrak
		#self.sk = np.array([179], dtype=np.int64)
		self.k = len(self.sk)
		#print("PK = "+str(self.sk))
		
	def calcula_x(self):
		firma = [ i-1 for i in list(generador_módulo_aleatorio(1, 3))]
		rlist = list(generador_módulo_aleatorio(1, self.n))
		self.r = rlist[0]
		rsq = self.r**(2, self.n)
		if(firma[0] == 0):
			return rsq
		else:
			return self.n-rsq
		
	def calcula_y(self, alist):
		y = mod(1, self.n)
		y = y*self.r
		for i in range(self.k):
			y = y*self.sk[i]**(alist[i], self.n)
		assert y.all() < self.n
		return y
		

class Bob:
	#Entidad que verifica el correcto funcionamiento de las pruebas de cero conocimeinto
	def __init__(self, n, vk):
		self.n = n
		self.vk = vk
		self.k = len(vk)
		#print(self.vk)
		
	def elige_a(self, x):
		self.abort = 0
		if x.all() == 0:
			self.abort = 1
			return []
		self.x = x
		self.a = [ i-1 for i in list(generador_módulo_aleatorio(k, 3))]
		#print(self.a)
		return self.a
	
	def autentificación(self, y):
		ysq = y**(2, self.n)
		#print("y^2 valor a ser comprobado = " + str(ysq))
		yrhs = mod(1, self.n)
		yrhs = yrhs*self.x
		for i in range(self.k):
			yrhs = yrhs*self.vk[i]**(self.a[i], self.n)
		if yrhs.all() == ysq.all() or yrhs.all() == self.n-ysq.all():
			return 0
		else:
			return 1


class ZeroKnowledgeProofTestParams():
	resultadoFinalParaVista = []
	def __init__(self, modbits, k, semilla, iterations, p, g):
		zeroKnowledgeProof_generator = testSetUp(modbits, k, semilla,p,g)

		alice = Alice(zeroKnowledgeProof_generator.n, p, g)
		bob = Bob(zeroKnowledgeProof_generator.n, zeroKnowledgeProof_generator.asq)
		#Comienzo del protocolo
		resultadoFinal = []
		resultadoFinal.append("------------------- VARIABLES DE LAS PRUEBAS -------------------")
		resultadoFinal.append("Original P: " + str(p))
		resultadoFinal.append("Original G: " + str(g))
		resultadoFinal.append("--------------------------------------")
		resultadoFinal.append("p prime: " + str(zeroKnowledgeProof_generator.p))
		resultadoFinal.append("q: " + str(zeroKnowledgeProof_generator.q))
		resultadoFinal.append("n: " + str(zeroKnowledgeProof_generator.n))
		resultadoFinal.append("a: " + str(zeroKnowledgeProof_generator.a[0]))

		resultadoFinal.append("------------------- INICIALIZANDO LAS PRUEBAS -------------------")
		i = 0
		abort = 0
		while (i < iterations and abort == 0):
			#print("------------------- Iteración número " + str(i+1) + " ------------------")
			resultadoFinal.append("------------------- Iteración número " + str(i+1) + " ------------------" )
			x = alice.calcula_x()
			alist = bob.elige_a(x)
			if not alist:
				#print("x es 0, no se puede proceder. Autentificación fallida.")
				resultadoFinal.append("x es 0, no se puede proceder. Autentificación fallida.")
				abort = 1
			else:
				y = alice.calcula_y(alist)
				ysq = y**(2, bob.n)
				#print("y^2 valor a ser comprobado = " + str(ysq))
				resultadoFinal.append("y^2 valor a ser comprobado = " + str(ysq))

				abort = bob.autentificación(y) 
			if(abort == 1):
				#print("Fallo en la iteración " + str(i+1))
				resultadoFinal.append("Fallo en la iteración " + str(i+1))
			i += 1
		#print("---------------------- FINALIZADO ------------------------")
		resultadoFinal.append("---------------------- FINALIZADO ------------------------")
		if abort == 0:
			#print("Autentificación satisfactoria. La prueba de Cero Conocimiento presentada por Alice es correcta.")
			resultadoFinal.append("Autentificación satisfactoria. La prueba de Cero Conocimiento presentada por Alice es correcta.")
			resultadoFinal.append("No se ha revelado información sobre el secreto a Bob durante el proceso.")
			#print("No se ha revelado información sobre el secreto a Bob durante el proceso.")
		elif abort == 1:
			#print("¡Autentificación FALLIDA! La prueba de Cero Conocimiento presentada por Alice es INCORRECTA.")
			resultadoFinal.append("¡Autentificación FALLIDA! La prueba de Cero Conocimiento presentada por Alice es INCORRECTA.")
		
		self.resultadoFinalParaVista = resultadoFinal

	def returnresultado(self):
		resultadoFinal = self.resultadoFinalParaVista
		return resultadoFinal


modbits = 256
k = 40
iterations = 20

# zkp = ZeroKnowledgeProofTestParams(modbits, k, semilla, iterations, p ,g)

