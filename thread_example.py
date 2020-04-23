import threading
compteur_global = 0
# Fonction principale des threads
def thread_main(nom) :
    global compteur_global

    for i in range(3):
        compteur_global += 1
        print("compteur = ", compteur_global)
    pass


# Fonction principale
t1 = threading.Thread( target=thread_main, args=("T1", ) )
t2 = threading.Thread( target=thread_main, args=("T2", ) )
t1.start()
t2.start()
t1.join()
t2.join()