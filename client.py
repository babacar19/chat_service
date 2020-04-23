import socket
import sys
import pickle
import threading

""" gestion des paramètres par defaut """

#-----------------------------------
""" definiition d'un moniteur pour tenter de gerer le parallelisme entre la reception et la messagerie """


class moniteur_client():
    def __init__(self):
        self.tmp = 1
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

#---------------------------------------------------------
moniteur = moniteur_client()
mutex = threading.Semaphore(1)
socket_connection = 0

class message:
    def __int__(self,msg=None,target = None):
        self.message = msg
        self.target = target
    def pick_msg(self):
        return pickle.dumps(self)


class Receveur(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #end

    def run(self):
        global socket_connection
        #mutex.acquire()

        try:
            data = socket_connection.recv(4096)
            print("reception message ..........")
        except ConnectionAbortedError:
            print("le server n'est plus en marche . Connection finie ")
            exit(1)

        msg = pickle.loads(data)
        print(">>>>>:received:  "+ msg.message )
        #mutex.release()


#---------------------------------------------------------------------------------#

class Envoyeur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global socket_connection
        moniteur.lock.acquire()

        m = message()
        m.target = input(" >>> ip target ?? ... : ")
        m.message = input(">>>> message:  ")
        data = m.pick_msg()
        try:
            socket_connection.sendall(data)
        except ConnectionAbortedError:
            print("le serveur ne marche plus . fin de la connection")
            exit(1)

        print(">>>:message envoyé ")
        #End
        moniteur.lock.release()
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