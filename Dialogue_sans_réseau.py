# Saisie initiale de l'ordinateur A
A = input("Ordinateur A : ")

# La boucle tourne tant que A ne demande pas l'arrêt
while A != "stop" and A != "0":

    # Saisie de l'ordinateur B
    B = input("Ordinateur B : ")

    # Si B tape 'stop' ou '0', on quitte LA BOUCLE IMMÉDIATEMENT
    if B == "stop" or B == "0":
        
        break

    # Nouveau message de l'ordinateur A
    A = input("Ordinateur A : ")

print("Fin de la conversation.")