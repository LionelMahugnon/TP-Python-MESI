#Importation de la bibliothèque
import socket

# Configuration 
HOST = "" # pour une écoute sur toutes les interfaces réseau
PORT = 5000 # Canal de communication

# Création du socket (IPv4, TCP)
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((HOST, PORT)) # Associe le socket à l'adresse et au port
serveur.listen(1)

print(f"SERVEUR (Ordinateur A) en attente sur le port {PORT} ")

connexion, adresse = serveur.accept() # En attente de la connexion avec ordinateur B

print(f"Connecté avec {adresse}\n")

while True:
    # Réception du message de B
    message_recu = connexion.recv(1024).decode("utf-8")

    if not message_recu or message_recu.lower() in ["stop", "0", " "]:
        print("L'ordinateur B a fermé la connexion.")
        break

    print(f"Ordinateur B : {message_recu}")

    # Saisie et envoi du message de A
    reponse = input("Ordinateur A : ").strip()
    connexion.send(reponse.encode("utf-8"))

    if reponse.lower() in ["stop", "0", " "]: # pour arreter la conversation
        print("Fermeture de la connexion par Ordinateur A.")
        break

connexion.close()
serveur.close()
print("Communication terminée.")