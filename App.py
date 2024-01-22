import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
from PIL import Image

# Fonction pour créer la table dans la base de données SQLite
def create_table():
    with sqlite3.connect("personnes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personnes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT,
                Materiel TEXT, 
                Appartenance TEXT,
                Langue TEXT,
                sexe TEXT,
                photo BLOB,
                telephone TEXT,
                is_admin INTEGER
            )
        """)

# Fonction pour insérer une personne dans la base de données
def insert_personne(nom, prenom, Materiel, Appartenance, Langue, sexe, photo, telephone, is_admin):
    with sqlite3.connect("personnes.db") as conn:
        cursor = conn.cursor()
        try:
            # Utilisation de paramètres pour éviter les injections SQL
            cursor.execute("""
                INSERT INTO personnes (nom, prenom, Materiel, Appartenance, Langue, sexe, photo, telephone, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nom, prenom, Materiel, Appartenance, Langue, sexe, photo, telephone, is_admin))
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"Erreur lors de l'insertion dans la base de données: {e}")

# Fonction pour afficher la liste des personnes
def display_personnes(is_admin):
    if is_admin:
        with sqlite3.connect("personnes.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM personnes")
                personnes = cursor.fetchall()
                return personnes
            except sqlite3.Error as e:
                st.error(f"Erreur lors de la récupération des données: {e}")
    else:
        return None

# Fonction pour récupérer les données sous forme de DataFrame
def get_dataframe():
    create_table()  # Assurez-vous que la table existe dans la base de données
    with sqlite3.connect("personnes.db") as conn:
        query = "SELECT * FROM personnes"
        df = pd.read_sql(query, conn)
    return df

# Interface utilisateur Streamlit
def main():
    st.title("Enregistrement des informations des personnes")

    # Formulaire pour saisir les informations
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    Materiel = st.radio("Matériel", ["Oui", "Non"])
    Appartenance = st.selectbox("Appartenance", ("BH EIOA", "BH Bakoura", "Band Organisé"))
    Langue = st.selectbox("Langue", ("Kanouri", "Haoussa", "Peulh", "Toubou", "Arabe"))
    sexe = st.radio("Sexe", ["Homme", "Femme"])
    photo = st.file_uploader("Photo", type=["jpg", "jpeg", "png"])
    telephone = st.text_input("Téléphone")
    is_admin = st.checkbox("Administrateur")

    # Bouton pour enregistrer les informations
    if st.button("Enregistrer"):
        if nom and prenom and sexe and telephone:
            # Convertir l'image en BLOB (binary large object) pour stockage dans SQLite
            if photo:
                photo_blob = photo.read()
            else:
                photo_blob = None

            # Enregistrer la personne dans la base de données
            insert_personne(nom, prenom, Materiel, Appartenance, Langue, sexe, photo_blob, telephone, is_admin)
            st.success("Enregistrement réussi!")

    # Afficher la liste des personnes enregistrées (uniquement pour les administrateurs)
    if is_admin:

        # Demander le mot de passe avant d'autoriser l'exportation vers Excel
        password = st.text_input("Mot de passe (pour l'exportation vers Excel)", type="password")
        if st.button("Exporter vers Excel") and password == "aziz":
            st.header("Liste des personnes enregistrées")
            personnes = display_personnes(is_admin)
            if personnes:
                for personne in personnes:
                    if len(personne) >= 9:
                        st.write(f"ID: {personne[0]}, Nom: {personne[1]}, Prénom: {personne[2]}, Sexe: {personne[6]}, Appartenance: {personne[4]}, Téléphone: {personne[8]}, Admin: {personne[9]}")
                        if personne[7] is not None:
                            image = Image.open(BytesIO(personne[7]))
                            st.image(image, caption=f"Photo de {personne[1]} {personne[2]}", use_column_width=True)
                    else:
                        st.warning("Le tuple personne n'a pas suffisamment d'éléments.")

            df = get_dataframe()
            excel_data = BytesIO()
            df.to_excel(excel_data, index=False, sheet_name='Personnes', engine='openpyxl')
            excel_data.seek(0)
            st.download_button(
                label="Télécharger le fichier Excel",
                data=excel_data,
                file_name="personnes.xlsx",
                key="export_excel_button"
            )

if __name__ == "__main__":
    main()
