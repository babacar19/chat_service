import socket #module necessaire pour la creation et utilisation des sockets
import threading
import  select
import pickle
#-------------------------------------------------
"""

--le serveur ne fait que recevoir des requêtes de message préfixées par un @ suivi du nom de la machine cible
--Le serveur doit aussi mettre à jour tous les clients sur le nombre de clients connectés

"""

"""

dico [ (ip , conn , id )]

"""


class message:
    def __int__(self,msg=None,target = None):
        self.message = msg
        self.target = target
    def pick_msg(self):
        return pickle.dumps(self)


clients_connectes = 0

class Receveur(threading.Thread):
    def __int__(self, socClient, clients):
        threading.Thread.__init__(self)
        self.sockClient = socClient
        self.client_connectes = clients

    def run(self):

        data = self.sockClient.recv(4096)
        msg = pickle.loads(data)
        print("message recu : " + msg.message)
        """"""
        target = msg.target
        for client in self.client_connectes:
            print("comparaison ",client[1][0],target)
            if client[1] == target:
                msg_obj = msg.pick_msg()
                client[0].sendall(msg_obj)
            break
        pass





#--------------------------------------------------


host, port = ('', 5566 ) #on definit l'adresse de l'hote et le port que l'on va utiliser

socket_reception = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creation de notre socket
socket_reception.bind((host, port)) #on attache notre socket à une adresse en préécisant le port

print("creation de socket et binding du socket ")


fin = 0

socket_reception.listen(5) #le nombre donné en argument correspond le nombre d'essais disponible avant de refuser la conection ; cette methode est un appel bloquant
print("serveur en ecoute ")


serveurLance = True
connection_en_cours = []


while serveurLance:

    #ecoutons les clients connectés avec select
    clients_connectes,wlist, xlist = select.select([socket_reception],[],[],9)

    for client in clients_connectes:
        my_client , host = client.accept()
        connection_en_cours.append((my_client,host[0]))

    for client in connection_en_cours:
        if client:

            traiteur = Receveur()
            traiteur.sockClient = client[0]
            traiteur.client_connectes = connection_en_cours
            traiteur.start()



    """for client in client_a_traiter:
        traiteur = Receveur(client[0] ,client[1])
        traiteur.start()"""

    """conn, adr = socket_reception.accept()#on accepte la connection; cette méthode renvoie un tuple contenant la connection et l'adresse
    print("connection établie ")
    while fin!=1:
        #reception de la donnee encodée

        try:
            data = conn.recv(1024)  # cette méthode prend en parameetre la taille du buffer , mais aussi des valeurs pour les flags , cf documentation
            if data == b'fin':
                fin = 1
                # endIf
            data = data.decode('utf-8')
        except ConnectionResetError:
            print(" connection coupée ")
            exit(1)

        print(data)
        msg= "reçu 5/5 ".encode('utf-8')
        conn.sendall(msg)"""
    #end (...for the moment )



socket_reception.close()
