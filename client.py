import socket
import sys
from info_client import *
import threading

""" gestion des paramètres par defaut """

mutex = threading.Semaphore(1)
socket_connection = 0

class Receveur(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #end

    def run(self):
        global socket_connection
        #mutex.acquire()
        print("reception message ..........")
        try:
            data = socket_connection.recv(1024)
        except ConnectionAbortedError:
            print("le server n'est plus en marche . Connection finie ")
            exit(1)

        data = data.decode('utf-8')
        print(">>>>>:received:  ",data )
        #mutex.release()


#---------------------------------------------------------------------------------#

class Envoyeur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global socket_connection
        mutex.acquire()
        with my_lock:
            data = input(">>>>:  ")
            try:
                socket_connection.sendall(data.encode('utf-8'))
            except ConnectionAbortedError:
                print("le serveur ne marche plus . fin de la connection")
                exit(1)

            print(">>>:message envoyé ")
            #End
        mutex.release()
#---------------------------------------------------------------------------------#

ip_sever = '10.188.4.88'
default_port_emsission = 5566



#(nom, prenom) = get_name()#gestion du client

print(sys.argv) #affichage des commandes lancées en ligne de  commande

try:
    host, port_emission = (sys.argv[1],int(sys.argv[2]))
    ip_sever = sys.argv[1]

except IndexError:
    host , port_emission = (ip_sever , default_port_emsission)


except:
    exit(1)

print("ordinateur cible : ",ip_sever)

""" creation du socket et tentative de conncection au serveur """
socket_connection = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
socket_connection.connect((ip_sever,port_emission))

#aprés acceptation de la connection par le seveur


while True:
    cli = Envoyeur()
    rec = Receveur()
    cli.start()
    rec.start()
    cli.join()
    rec.join()

"""fermeture des sockets :: important """
socket_connection.close()