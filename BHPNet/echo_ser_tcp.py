import socket, sys

PORT = 50001

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

#Creamos el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dir_serv = (sys.argv[1], PORT)
#Asociamos la direccion y el puerto al socket
s.bind(dir_serv)
s.listen(2)

while True:
	conn, dir_cli = s.accept()
	mensaje = conn.recv(1024).decode()
	
	conn.sendto(mensaje.encode(), dir_cli)

s.close()
