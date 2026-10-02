# Importation des bibliothèques
import tkinter as tk
from tkinter import messagebox

# Création de la Fenêtre principale
fenetre = tk.Tk()
fenetre.title("Calculatrice")

# Définition de la Fonction Calculatrice
def calculer(operation):
    try : #afin d'intercepter les erreurs pour ne faire planter le programme
        N1 = float (entree1.get()) #entrée du premier nombre
        N2 = float (entree2.get()) #entrée du second nombre

        if operation == "+":
            Ans = N1+N2
        elif operation == "-" :
            Ans = N1-N2
        elif operation == "*":
            Ans = N1*N2
        elif operation == "/":
            if N2==0 : #Cas où l'utilisateur entre un 0 au dénominateur pour la division
                Resultat.config(text="Erreur : division par zéro. Impossible !", fg='red')
                return
            else:
                Ans =  N1 / N2

        Resultat.config(text=f"Resultat : {Ans}", fg='green')
        
    except ValueError: #Renvoie ce texte en cas d'erreur d'entrée notamment détection de lettre ou autre
        Resultat.config(text="Erreur : veuillez taper des nombres valides svp !", fg='red')  
        return



# Creation de la première fenetre pour entrer le premier nombre
entree1 = tk.Entry(fenetre)

# Widgets pour l'entrée 1
tk.Label(fenetre, text="Premier nombre :").grid(row=0, column=0)
entree1.grid(row=0, column=1) #pour la disposition 

#  Creation de la première fenetre pour entrer le deuxième nombre
entree2 = tk.Entry(fenetre)

# Widgets pour l'entrée 2
tk.Label(fenetre, text="Deuxième nombre :").grid(row=1, column=0)
entree2.grid(row=1, column=1)


# Création des Boutons(+, -, /, *) pour les opérations
# Une autre fenetre (Frame) pour centrer les boutons
frame_boutons = tk.Frame(fenetre)

# Disposition de la fenetre centrer par rapport au deux dernières lignes
frame_boutons.grid(row=2, column=0, columnspan=2, pady=10)

# Les boutons sont placés à l'intérieur du Frame côte à côte
tk.Button(frame_boutons, text="+", width=5, command=lambda: calculer("+")).pack(side="left", padx=3)
tk.Button(frame_boutons, text="-", width=5, command=lambda: calculer("-")).pack(side="left", padx=3)
tk.Button(frame_boutons, text="*", width=5, command=lambda: calculer("*")).pack(side="left", padx=3)
tk.Button(frame_boutons, text="/", width=5, command=lambda: calculer("/")).pack(side="left", padx=3)

#Affichage du résulat
Resultat = tk.Label(fenetre, text="Résultat : ", fg='green')
Resultat.grid(row=4, column=0, columnspan=4, pady=10)
fenetre.mainloop()
