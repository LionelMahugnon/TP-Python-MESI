# Importation des bibliothèques
from email.message import EmailMessage
import csv
import getpass
import smtplib
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import schedule

# Variables globales
expediteur = "" # pour le mail de l'expéditeur
destinataire = "" # pour le mail du destinataire
mot_de_passe = "" # le mot de passe de l'expéditeur


# FONCTIONS DE TRAITEMENT
#1- Fonction de lecture et classification des produits critiques
def lire_produits_critiques():
    """Lit le CSV et retourne la liste des produits en alerte."""
    produits_critiques = []
    try:
        with open("TP2_inventaire.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Saut de l'en-tête
            for row in reader:
                nom = row[0] # première colonne pour les noms
                quantite = int(row[1]) # deuxième pour les quantités mais convertit en entier
                seuil = int(row[2]) # 3e pour les seuils
                if quantite < seuil:
                    produits_critiques.append((nom, quantite, seuil))
    except Exception as e: # Cas où on ne peut pas lire le fichier
        messagebox.showerror(
            "Erreur CSV", f"Impossible de lire le fichier CSV :\n{e}"
        )
    return produits_critiques

# 2- Fonction pour la génération du rapport txt
def generer_rapport_texte():
    """Génère le fichier rapport.txt à partir du CSV."""
    try:
        produits_critiques = []
        produits_nocritiques = []

        with open("TP2_inventaire.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                nom = row[0]
                quantite = int(row[1])
                seuil = int(row[2])
                if quantite < seuil:
                    produits_critiques.append((nom, quantite, seuil))
                else:
                    produits_nocritiques.append((nom, quantite, seuil))

        with open("rapport.txt", "w", encoding="utf-8") as f:
            f.write("Rapport d'inventaire\n_____________________\n")
            f.write("Produits en stock :\n")
            for nom, qty, _ in produits_nocritiques:
                f.write(f"- {nom} : {qty} unités\n")
            f.write("\nProduits en alerte :\n")
            for nom, qty, seuil in produits_critiques:
                f.write(f"- {nom} : {qty} unités (Seuil : {seuil})\n")

        # Message de confirmation
        messagebox.showinfo(
            "Succès", "Le rapport 'rapport.txt' a été généré avec succès !"
        )
        return True
    except Exception as e: # Cas où le rapport n'a pas pu etre généré
        messagebox.showerror(
            "Erreur", f"Erreur lors de la génération du rapport :\n{e}"
        )
        return False

#3- Fonction pour l'envoi du mail
def envoyer_email_action():
    """Envoie du rapport par mail avec les adresses saisies."""
    global expediteur, destinataire, mot_de_passe

    expediteur = entry_exp.get().strip()
    destinataire = entry_dest.get().strip()
    mot_de_passe = entry_mdp.get().strip()

    # Cas de message vide au niveau des entrées
    if not expediteur or not destinataire or not mot_de_passe: 
        messagebox.showwarning( "Champs manquants", "Veuillez remplir tous les champs e-mail et MDP.")
        return

    # S'assure que le rapport existe avant l'envoi
    if not generer_rapport_texte():
        return

    msg = EmailMessage()
    msg["Subject"] = "Rapport d'inventaire (GUI)"
    msg["From"] = expediteur
    msg["To"] = destinataire
    msg.set_content(
        "Bonjour,\n\nVeuillez trouver ci-joint le rapport d'inventaire.\n\nCordialement."
    )

    #Definition de l'objet
    try:
        with open("rapport.txt", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="plain",
                filename="rapport.txt",
            )

        # envoi unique par gmail, pas possible avec le mail d'unistra
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(expediteur, mot_de_passe)
            smtp.send_message(msg)

        messagebox.showinfo("E-mail envoyé", "L'e-mail a été envoyé avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur d'envoi", f"Échec de l'envoi :\n{e}")


# 4- Gonction pour le schedule d'envoi du mail
def planifier_tache():
    """Planification de l'envoi du mail"""
    schedule.clear()
    schedule.every().day.at("18:18").do(envoyer_email_action)

    # Lancement de la boucle schedule séparement pour ne pas bloquer Tkinter
    def boucle_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=boucle_schedule, daemon=True)
    t.start()

    # Message de confirmation 
    lbl_statut_planif.config(
        text="Status : Tâche planifiée tous les jours à 18h18.", fg="green"
    )
    messagebox.showinfo("Planification", "La tâche est planifiée pour 18h18 !")


#INTERFACE GRAPHIQUE (Tkinter)
root = tk.Tk()
root.title("Gestionnaire d'Inventaire")
root.geometry("500x650") # geometrie plus grande

# Affichage des produits en alerte dans une liste
frame_product = tk.LabelFrame(
    root, text="Produits en alerte", padx=10, pady=10
)
frame_product.pack(fill="x", padx=10, pady=5) 

listbox_alertes = tk.Listbox(frame_product, height=5)
listbox_alertes.pack(fill="x")

# Chargement initial des données dans la Listbox
alertes = lire_produits_critiques()
if alertes:
    for nom, qty, seuil in alertes:
        listbox_alertes.insert(
            tk.END, f"⚠️ {nom} - Stock : {qty} (Seuil : {seuil})"
        )
else:
    listbox_alertes.insert(tk.END, "Aucun produit en alerte.")

# Bouton pour générer le rapport txt
frame_rapport = tk.LabelFrame(
    root, text=" Génération de rapport", padx=10, pady=10
)
frame_rapport.pack(fill="x", padx=10, pady=5)

btn_generer = tk.Button(
    frame_rapport,
    text="Générer le rapport texte",
    command=generer_rapport_texte,
    bg="#e1e1e1",)
btn_generer.pack()

# Saisie e-mail et bouton d'envoi
frame_email = tk.LabelFrame(
    root, text=" Saisie E-mail & Envoi", padx=10, pady=10
)
frame_email.pack(fill="x", padx=10, pady=5)

 # fenetre pour editer l'adresse de l'expéditeur
tk.Label(frame_email, text="Expéditeur :").grid(row=0, column=0, sticky="w")
entry_exp = tk.Entry(frame_email, width=35)
entry_exp.grid(row=0, column=1, pady=2)

# fenetre pour editer l'adresse du dessinataire
tk.Label(frame_email, text="Destinataire :").grid(row=1, column=0, sticky="w")
entry_dest = tk.Entry(frame_email, width=35)
entry_dest.grid(row=1, column=1, pady=2)

# fenetre pour editer le mot de passe
tk.Label(frame_email, text="Mot de passe d'app :").grid(
    row=2, column=0, sticky="w"
)

entry_mdp = tk.Entry(frame_email, show="*", width=35) # pour un affichage d'étoile à la place du mot de passe visible
entry_mdp.grid(row=2, column=1, pady=2)

# bouton pour envoyer le mail
btn_envoyer_mail = tk.Button(
    frame_email,
    text="Envoyer le rapport par mail",
    command=envoyer_email_action,
    fg="white",
)
btn_envoyer_mail.grid(row=3, columnspan=2, pady=10)

# Bouton de planification de l'envoi
frame_plan = tk.LabelFrame(
    root, text=" Planification", padx=10, pady=10
)
frame_plan.pack(fill="x", padx=10, pady=5)

btn_planifier = tk.Button(
    frame_plan,
    text="Planifier l'envoi quotidien (18:18)",
    command=planifier_tache,
)
btn_planifier.pack()

# retour sur l'état de la planification
lbl_statut_planif = tk.Label(
    frame_plan, text="Status : Aucune tâche planifiée", fg="red"
)
lbl_statut_planif.pack(pady=5)

root.mainloop()

