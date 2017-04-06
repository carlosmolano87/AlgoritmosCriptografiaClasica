#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import Utilidad as util
import threading
import sys
import os
import time
from itertools import zip_longest

class Trasposicion(object):
	def __init__(self, cadena):
		self.cadena = cadena
		self.bloque1 = list()
		self.bloque2 = list()

	def cifrarTexto(self):
		textoCifrado = ""
		saltosLinea = len(self.cadena)-1
		i = 0
		for linea in self.cadena:
			if i < saltosLinea:
				textoCifrado = textoCifrado + self.__cifrarTexto(linea) + "\n"
				i = i+1
			else:
				textoCifrado = textoCifrado + self.__cifrarTexto(linea)
		return textoCifrado

	def descifrarTexto(self):
		textoDescifrado = ""
		saltosLinea = len(self.cadena)-1
		i = 0
		for linea in self.cadena:
			if i < saltosLinea:
				textoDescifrado = textoDescifrado + self.__descifrarTexto(linea) + "\r\n"
				i = i+1
			else:
				textoDescifrado = textoDescifrado + self.__descifrarTexto(linea)
		return textoDescifrado

	def __cifrarTexto(self,linea):
		i = 0
		longitudCadena = len(linea)
		while i < longitudCadena:
			if i%2 == 0:
				self.bloque1.append(linea[i])
			else:
				self.bloque2.append(linea[i])
			i = i+1
		textoBloque1 = ''.join(self.bloque1)
		textoBloque2 = ''.join(self.bloque2)
		textoCifrado = textoBloque1+textoBloque2

		self.__vaciarLista(self.bloque1)
		self.__vaciarLista(self.bloque2)
		return textoCifrado

	def __descifrarTexto(self,linea):
		i = 0
		longitudCadena = len(linea)
		mitad = longitudCadena/2

		#Llenar los bloques con sus mitades
		while i < mitad:
			self.bloque1.append(linea[i])
			i = i+1
		while i < longitudCadena:
			self.bloque2.append(linea[i])
			i = i+1

		#Intercalar caracteres
		textoClaro = []
		i = 0
		for a,b in zip_longest(self.bloque1, self.bloque2):
			if a == None:
				textoClaro.append('')
			else:
				textoClaro.append(a)
			if b == None:
				textoClaro.append('')
			else:
				textoClaro.append(b)
		self.__vaciarLista(self.bloque1)
		self.__vaciarLista(self.bloque2)
		return ''.join(textoClaro)

	def __vaciarLista(self,lista):
		del lista[:]


#-----------------------------------------------------------------------------------------
tiempo_ini = time.time()
util = util.Utilidad()
archivo = sys.argv[1]
nombre, extension, cod, so = util.obtenerMetadatos(archivo)
util.crearArchivoMetadatos(nombre, extension, cod, so)

hilo = threading.Thread(target=util.resolverCodificacion(cod,"UTF-8",archivo,"tmp"))
hilo.start()
time.sleep(2/1000)
#util.resolverCodificacion(cod,"UTF-8",archivo,"tmp")

archivoUTF = open("./salida/tmp", "r")
cadena = archivoUTF.read().split("\n")
archivoUTF.close()
os.remove("./salida/tmp")

tSimple = Trasposicion(cadena)
criptograma = tSimple.cifrarTexto()
#print(criptograma)

util.crearArchivoCifrado(nombre+extension,criptograma)
tiempo_fin = time.time() - tiempo_ini
print("Tiempo -> ",tiempo_fin)

# ------------------------------------------------------------DESCIFRAR---------------------
archivoCIF = open("./salida/"+nombre+extension+".CIF", "r")
cadena = archivoCIF.read().split("\n")
archivoCIF.close()

tSimple.cadena = cadena
textoClaro = tSimple.descifrarTexto()

archivoDES = open("./salida/tmp", "w")
archivoDES.write(textoClaro)
archivoDES.close()
time.sleep(2/1000)

util.resolverCodificacion("UTF-8",cod, "./salida/tmp",nombre+extension)
time.sleep(2/1000)
os.remove("./salida/tmp")