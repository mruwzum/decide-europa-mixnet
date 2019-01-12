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

from .test_zkp import ZeroKnowledgeProofTest as ZkpAutomated

from .test_zkp_withParams import ZeroKnowledgeProofTestParams as ZkpParams

from .forms import *

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
			
def vistaSimetrica(request):
	form = ValorSimetrico(request.GET) #definiendo aquí el methodo request.GET se consigue el valor del formulario
	palabra = form['p'].value()

	print(palabra)

	if(palabra is None):
		palabra = "                "
	
	if(len(palabra) < 16):
		palabra = palabra + "                      "

	if(len(palabra) > 16):
		palabra = palabra[0:16]
	


	lista = []
	#texto = b"palabra         "
	
	b = bytes(palabra, 'utf-8')
	texto = b
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
	context = {'pruebas':lista, 'form':form}
	
	return render(request, 'simetrico.html', context)
	
primePrime = sympy.randprime(0, 9999999999)
semilla = int(round(time.time() * primePrime))
modbits = 256
k = 40
iterations = 20

def vistaZkp(request):
	zkpA = ZkpAutomated(modbits, k, semilla, iterations)
	context = {'pruebas':zkpA.returnresultado()}
	return render(request, 'zkp.html', context)

def menu(request):
	pruebas = ['hola', 'adios']
	context = {'pruebas':pruebas}
	return render(request, 'menu.html', context)

def cargarpk(request):
	primePrime = sympy.randprime(0, 9999999999)
	semilla = int(round(time.time() * primePrime))
	modbits = 256
	k = 40
	iterations = 20
	form = ValoresForm(request.GET)
	if form.is_valid():
		form.save()
	p = form['p'].value()
	g = form['g'].value()

	if p is None:
		p = 133
	if g is None:
		g = 21

	zkpB = ZkpParams(modbits, k, semilla, iterations, p , g)
	context = {'pruebas':zkpB.returnresultado(),'form':form}
	return render(request,'cargarPk.html',context)


