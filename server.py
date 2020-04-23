import socket #module necessaire pour la creation et utilisation des sockets


host, port = ('', 5566 ) #on definit l'adresse de l'hote et le port que l'on va utiliser

socket_reception = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creation de notre socket
socket_reception.bind((host, port)) #on attache notre socket à une adresse en préécisant le port

print("creation de socket et bindind complete ")


fin = 0

socket_reception.listen(5) #le nombre donné en argument correspond le nombre d'essais disponible avant de refuser la conection ; cette methode est un appel bloquant
print("serveur en ecoute ")
while True and fin != 1:

    conn, adr = socket_reception.accept()#on accepte la connection; cette méthode renvoie un tuple contenant la connection et l'adresse
    print("connection établie ")
    while fin!=1:
        #reception de la donnee encodée
        data = conn.recv(1024) #cette méthode prend en parameetre la taille du buffer , mais aussi des valeurs pour les flags , cf documentation
        if data == b'fin':
            fin = 1
            #endIf
        try:
            data = data.decode('utf-8')
        except ConnectionResetError:
            print(" connection coupée ")
            exit(1)

        print(data)
        msg= "reçu 5/5 ".encode('utf-8')
        conn.sendall(msg)
    #end (...for the moment )


conn.close()
socket_reception.close()
