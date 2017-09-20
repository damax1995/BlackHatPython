#!/usr/bin/env python3

import socket, sys

PORT = 50001

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL ALUMNO:
Crear el socket.
"""
dir_serv = (sys.argv[1], PORT)

s = socket.socket( socket.AF_INET,socket.SOCK_DGRAM )

print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	ms = ""
	if not mensaje:
		break
	"""A COMPLETAR POR EL ALUMNO:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	"""
	
	#SIN DIVIDIR EN PAQUETES
	#s.sendto( mensaje.encode(), dir_serv)
	#buf = s.recv( 1024 )
	#print( "Datos recibidos del servidor:", buf.decode() )

	#DIVIDIENDO EN PAQUETES
	i = 1
	while (len(mensaje.encode())>=10):
		m = mensaje.encode()[0:9]
		s.sendto(m, dir_serv)
		buf = s.recv(10)
		print("Dato "+str(i)+" recibidos del servidor: ", buf.decode())	
		ms = ms + m.decode()	
		mensaje = mensaje[9:]
		i = i+1
	
	if len(mensaje.encode()):
		s.sendto(mensaje.encode(), dir_serv)
		buf = s.recv(10)
		print("Dato "+str(i)+" recibidos del servidor: ", buf.decode())
		ms = ms + mensaje

	print("El paquete completo contiene: "+ms)
			
	
"""A COMPLETAR POR EL ALUMNO:
Cerrar socket.
"""
s.close()
