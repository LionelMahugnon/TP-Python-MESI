# Importation de la bibliothèque
import socket

# Configuration 
HOST = "127.0.0.1" # adresse local 
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT)) #connexion à l'ordinateur A
    print("### CLIENT (Ordinateur B) connecté au serveur ###")
    print("Tapez 'stop' ou '0' pour quitter.\n")

    while True:
        # Saisie et envoi du message de B
        message = "" # au cas où le message ne contient pas de texte
        while not message:
            message = input("Ordinateur B : ").strip()

            # Envoi uniquement si le message contient du texte
            client.send(message.encode("utf-8"))
       

        if message.lower() in ["stop", "0"]:
            print("Fermeture de la connexion...")
            break

        # Attente de la réponse de A
        reponse = client.recv(1024).decode("utf-8") # dechiffrage du message entré

        if not reponse or reponse.lower() in ["stop", "0"]: # cas où l'ordinateur A décide d'arreter
            print("L'ordinateur A a fermé la connexion.")
            break

        print(f"Ordinateur A : {reponse}")

except ConnectionRefusedError: # Au cas où il n'arrive pas se connecteur
    print(
        "Impossible de se connecter. Vérifiez que le serveur (Ordinateur A) est bien lancé."
    )

finally:
    client.close()
    print("Communication terminée.")