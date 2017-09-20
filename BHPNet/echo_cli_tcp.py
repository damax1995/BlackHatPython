import socket, sys

PORT = 50001

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )
dir_serv = (sys.argv[1], PORT)

#Creamos el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conectamos el cliente al servidor
s.connect(dir_serv)

#Gestionamos info
print("Introduce el mensaje que quieres enviar (vacio = fin): ")
while True:
	mensaje = input()
	if not mensaje:
		break
	
	#Mandamos el mensaje al server
	s.send(mensaje.encode())
	#Recibimos respuesta del server
	buf = s.recv(1024)
	print("Datos recibidos del servidor: " + buf.decode())

s.close()
