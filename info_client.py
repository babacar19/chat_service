"""
ce module est destiné à gerer plus tard les informations du client

"""
import threading
import socket

socket_reception = 0
socket_emission = 0



def get_name():
    nom = input("Donnez votre nom : ")
    prenom = input("Donnez votre prenom : ")

    return (nom,prenom)

"""

* sock: le socket de reception 
 
"""
my_lock = threading.RLock()

class client_server(threading.Thread):
    def __init__(self ,port_reception ):
        global socket_reception
        threading.Thread.__init__(self)
        socket_reception = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_reception.bind(('',port_reception))

    def run(self):
        global socket_reception
        while True:
            socket_reception.listen(5)
            conn,adr = socket_reception.accept()
            print("Connection reussie avec : ",adr[0])
            data = conn.recv(1024)
            data = data.decode('utf8')
            print("message : ",data)
            #je suppose que c'est un thread  qui gère cela done je n'essaie pas de sotir de la boucle  pour l'instant
        pass

    def close(self):
        socket_reception.close()


class client_gestion(threading.Thread):
    def __init__(self ,args ):
        global socket_emission
        threading.Thread.__init__(self)
        socket_emission = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_emission.connect((args[0],args[1]))

    def run(self):
        global socket_emission
        with my_lock:
            while True:
                data = input("ecrire votre message: ")
                data = data.encode('utf8')
                socket_emission.sendall(data)

        pass

    def close(self):
        socket_emission.close()