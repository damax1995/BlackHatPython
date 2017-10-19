#!/usr/bin/env python3
# coding=utf-8

import socket, os, signal

PORT = 50004
camara = False

"""NOTA:
Los números de los comentarios (entre paréntesis) identifican distintos
ejercicios. Es necesario realizar los distintos ejercicios de uno en
uno, probando su correcto funcionamiento antes de pasar al siguiente.
"""

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

s.bind( ('', PORT) )
s.listen( 5 )

"""A COMPLETAR POR EL ALUMNO:
(2) Evitar que procesos hijo queden como zombi.
Para ello habra que usar la funcion 'signal' para que trate
las señales tipo SIGCHLD.
"""
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
index = b"""COMANDOS POSIBLES:
		1) ON -> Enciende o apaga la camara, dependiendo del estado de la misma.
		2) HD -> Muestra el espacio libre en el disco.
		3) LS -> Muestra una lista de los videos disponibles.
		4) DW + id + video -> Descarga el video introducido.
		5) DL + id + video -> Elimina el video introducido."""

while True:
	dialogo, dir_cli = s.accept()
	dialogo.sendall(index)
	print( "Cliente conectado desde {}:{}.".format( dir_cli[0], dir_cli[1] ) )
	
	"""A COMPLETAR POR EL ALUMNO:
	(1) Crear un nuevo proceso que atienda al cliente recien conectado.
	Mientras, el proceso principal quedará a la espera de nuevas conexiones. 
	"""
	if os.fork():#si el fork nos devuelve algo distinto de 0, somos el padre y se cerrara el proceso
		dialogo.close()
	else:
		#cerramos el socket
		s.close()
		while True:
			buf = dialogo.recv( 1024 ).decode()
			if not buf:
				break
			elif buf[0:1] == "ON":
				if not camara:
					ans = b"Camara encendida."
					camara = True
				else:
					ans = b"Camara apagada."
					camara = False
			elif buf[0:1] == "HD":
				ans = b"Espacio libre en el disco: " #hemos de ver como ver el espacio libre del disco.
			elif buf[0:1] == "LS":
				ans = b"Videos disponibles: \n" #Obtener videos disponibles
			elif buf[0:1] == "DW":
				ans = b"Descargar video"
			elif buf[0:1] == "DL":
				ans = b"Borrar video"

			dialogo.sendall( ans )
			print( "Solicitud de cierre de conexión recibida." )
			dialogo.close()
			exit(0)
s.close()

