from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MixnetSerializer
from .models import Auth, Mixnet, Key
from base.serializers import KeySerializer, AuthSerializer

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from Crypto.Cipher import AES 
import binascii,os

import time
from numpy import mod
import numpy as np
import sympy
import random
from math import gcd
#entorno virtual source /home/naitcode/Escritorio/decide-europa-mixnet/decide-env/bin/activate
class MixnetViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows mixnets to be viewed or edited.
	"""
	queryset = Mixnet.objects.all()
	serializer_class = MixnetSerializer

	def create(self, request):
		"""
		This create a new mixnet and public key

		 * auths: [ {"name": str, "url": str} ]
		 * voting: id
		 * position: int / nullable
		 * key: { "p": int, "g": int } / nullable
		"""

		auths = request.data.get("auths")
		voting = request.data.get("voting")
		key = request.data.get("key", {"p": 0, "g": 0})
		position = request.data.get("position", 0)
		p, g = int(key["p"]), int(key["g"])

		dbauths = []
		for auth in auths:
			isme = auth["url"] == settings.BASEURL
			a, _ = Auth.objects.get_or_create(name=auth["name"],
											  url=auth["url"],
											  me=isme)
			dbauths.append(a)

		mn = Mixnet(voting_id=voting, auth_position=position)
		mn.save()

		for a in dbauths:
			mn.auths.add(a)

		mn.gen_key(p, g)

		data = { "key": { "p": mn.key.p, "g": mn.key.g } }
		# chained call to the next auth to gen the key
		resp = mn.chain_call("/", data)
		if resp:
			y = (resp["y"] * mn.key.y) % mn.key.p
		else:
			y = mn.key.y

		pubkey = Key(p=mn.key.p, g=mn.key.g, y=y)
		pubkey.save()
		mn.pubkey = pubkey
		mn.save()

		return  Response(KeySerializer(pubkey, many=False).data)


class Shuffle(APIView):

	def post(self, request, voting_id):
		"""
		 * voting_id: id
		 * msgs: [ [int, int] ]
		 * pk: { "p": int, "g": int, "y": int } / nullable
		 * position: int / nullable
		"""

		position = request.data.get("position", 0)
		mn = get_object_or_404(Mixnet, voting_id=voting_id, auth_position=position)

		msgs = request.data.get("msgs", [])
		pk = request.data.get("pk", None)
		if pk:
			p, g, y = pk["p"], pk["g"], pk["y"]
		else:
			p, g, y = mn.key.p, mn.key.g, mn.key.y

		msgs = mn.shuffle(msgs, (p, g, y))

		data = {
			"msgs": msgs,
			"pk": { "p": p, "g": g, "y": y },
		}
		# chained call to the next auth to gen the key
		resp = mn.chain_call("/shuffle/{}/".format(voting_id), data)
		if resp:
			msgs = resp

		return  Response(msgs)


class Decrypt(APIView):

	def post(self, request, voting_id):
		"""
		 * voting_id: id
		 * msgs: [ [int, int] ]
		 * pk: { "p": int, "g": int, "y": int } / nullable
		 * position: int / nullable
		"""

		position = request.data.get("position", 0)
		mn = get_object_or_404(Mixnet, voting_id=voting_id, auth_position=position)

		msgs = request.data.get("msgs", [])
		pk = request.data.get("pk", None)
		if pk:
			p, g, y = pk["p"], pk["g"], pk["y"]
		else:
			p, g, y = mn.key.p, mn.key.g, mn.key.y

		next_auths = mn.next_auths()
		last = next_auths.count() == 0

		# useful for tests only, to override the last value
		last = request.data.get("force-last", last)

		msgs = mn.decrypt(msgs, (p, g, y), last=last)

		data = {
			"msgs": msgs,
			"pk": { "p": p, "g": g, "y": y },
		}
		# chained call to the next auth to gen the key
		resp = mn.chain_call("/decrypt/{}/".format(voting_id), data)
		if resp:
			msgs = resp

		return  Response(msgs)

class zkpView(TemplateView): 
	template_name = "zkp.html"
	def get_context_data(self):
		context = super().get_context_data()
		return context


modbits = 256
k = 40
iterations = 20

primePrime = sympy.randprime(0, 9999999999)
semilla = int(round(time.time() * primePrime))

  
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


class testSetUp(object):
	#Inicialización de las variables que se van a utilizar a lo largo de la
	#ejecución de las pruebas de cero conocimiento.
	def __init__(self, modbits, k, semilla):
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
		self.a = list(generador_módulo_aleatorio(k,modbits))
		assert sum([gcd(i, self.n) for i in self.a]) == len(self.a)
		self.asq = [i**(2, self.n) for i in self.a]
		

class Alice(object):
	def __init__(self, n, sk):
		self.n = n
		self.sk = sk
		# self.sk = np.array([179,179,179,179], dtype=np.int64)
		#self.sk = np.array([179], dtype=np.int64)
		self.k = len(sk)
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

class Bob(object):
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
		# print("y^2 valor a ser comprobado = " + str(ysq))
		yrhs = mod(1, self.n)
		yrhs = yrhs*self.x
		for i in range(self.k):
			yrhs = yrhs*self.vk[i]**(self.a[i], self.n)
		if yrhs.all() == ysq.all() or yrhs.all() == self.n-ysq.all():
			return 0
		else:
			return 1



class ZeroKnowledgeProofTest():
	resultadoFinalParaVista = []
	def __init__(self, modbits, k, semilla, iterations):
		zeroKnowledgeProof_generator = testSetUp(modbits, k, semilla)
		alice = Alice(zeroKnowledgeProof_generator.n, zeroKnowledgeProof_generator.a)
		bob = Bob(zeroKnowledgeProof_generator.n, zeroKnowledgeProof_generator.asq)
		#Comienzo del protocolo
		resultadoFinal = []
		resultadoFinal.append("------------------- VARIABLES DE LAS PRUEBAS -------------------")
		resultadoFinal.append("p: " + str(zeroKnowledgeProof_generator.p))
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

		

			
def vistaSimetrica(request):
	lista = []
	texto = b"CristianRodrigu "
	lista.append("Texto en claro: "+ str(texto)[2:][:-1])
	key = b"00112233445566778899aabbccddeeff"
	lista.append("Clave utilizada: "+ str(key)[2:][:-1])
	iv = os.urandom(16)
	lista.append("Vector de inicialización: "+ str(iv)[2:][:-1])
	aes_mode = AES.MODE_CBC
	obj = AES.new(key, aes_mode, iv)

	ciphertext = obj.encrypt(texto)
	print(ciphertext)
	lista.append("Texto cifrado: "+ str(ciphertext)[2:][:-1])


	cipher = AES.new(key, aes_mode, iv)
	plaintext = cipher.decrypt(ciphertext)
	print(plaintext)
	lista.append("Texto en plano descifrado: "+str(plaintext)[2:][:-1]) 
	if(plaintext == texto):
		lista.append("Prueba realizada con exito, las cadenas coinciden")   
	context = {'pruebas':lista}
	
	return render(request, 'simetrico.html', context)
	

	
def vistaZkp(request):
		zkp2 = ZeroKnowledgeProofTest(modbits, k, semilla, iterations)
		context = {'pruebas':zkp2.returnresultado()}
		return render(request, 'zkp.html', context)

def menu(request):
	pruebas = ['hola', 'adios']
	context = {'pruebas':pruebas}
	return render(request, 'menu.html', context)

