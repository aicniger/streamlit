import streamlit as st
import sqlite3
import re
from PIL import Image

def create_database():
    # Connexion à la base de données (crée automatiquement si elle n'existe pas)
    conn = sqlite3.connect('feedback1.db')
    c = conn.cursor()

    # Création de la table feedback
    c.execute('''CREATE TABLE IF NOT EXISTS feedback1(id integer primary key autoincrement unique,adresse_mail varchar(60),lieu_viste text,satisfaction text,
    satisfaction_generale integer,previsite text,space_pre text,question_realisa text,Vous_avez_vu tex,votre_att text,orientatio text,constat_prischg tetx,jsutification_prischg tetx,comment text)''')

    # Enregistrement des modifications et fermeture de la connexion
    conn.commit()
    conn.close()

# Création de la base de données et de la table
create_database()

# Création de la page d'accueil
image_file =Image.open("Logo_santraplus.png")
st.image(image_file, width=200)

st.title("Questionnaire de satisfaction suite à votre visite")
st.write("Le sondage prendra environ 4 minutes.")
st.write("Dans le but d'améliorer votre prise en charge, merci de nous accorder un peu de votre temps.")

# Récupération des données du formulaire
adresse_mail=st.text_input("1.Votre Adresse Mail:")
lieu_viste=st.selectbox("2.Ou avez vous passé votre viste:",["","Gonfreville L'orcher","Lillebonne"])
satisfaction = st.selectbox("3.Niveau de satisfaction:", ["","Très insatisfait", "Insatisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"])
satisfaction_generale = st.slider("4.Etes-vous satisfait de maniére générale ? de 0 à 10:",min_value=0, max_value=10, value=5)
previsite = st.selectbox("5.Avez-vous passé une pré-visite sur table?:",["","Non","Oui"])
if previsite=="Oui":
    space_pre = st.selectbox("6.Concernant l'espace de pré-visite sur tablette, êtes-vous globalement satisfait de :",["","Disponibilité de l'assistante",
    "Compréhension du questionnaire","Espace de confidentialité","Matériel adapté"])
    question_realisa=st.slider("7.Etes vous globalement satisfait de votre échange avec le professionnel de santé ?",min_value=0, max_value=10, value=5)
    Vous_avez_vu = st.selectbox("8.Vous avez vu un:",["","Médecin","Infrime","Spécialiste"])
    votre_att=st.selectbox("9.Qu'attendez vous de votre service de santé au travail ?",["","Plus de prévention et d'action collective",
    "Plus de prévention et d'action individuelle","Plus d'accompagnement et d'orientation vers spécialiste (nutritionniste, psychologue...)",
    "Je n'ai pas d'attentes particulières, je suis satisfait de mon suivi "])
    orientatio=st.text_input("10.Vers quel type de spécialiste souhaiteriez-vous être orienté dans le cadre de votre suivi santé au travail ? ")
    constat_prischg=st.selectbox("11.Constatez-vous une amélioration dans la prise en charge depuis votre dernière visite ? ",
    ["","Oui","Non"])
    if constat_prischg=="Oui":
        jsutification_prischg=st.text_input("12.Si oui, laquelle ?")
    else:
        jsutification_prischg=st.text_input("12.Si non, pourquoi ?")    
    comment = st.text_area("Votre avis nous intéresse:")
else :
    otre_att=st.selectbox("9.Qu'attendez vous de votre service de santé au travail ?",["","Plus de prévention et d'action collective",
    "Plus de prévention et d'action individuelle","Plus d'accompagnement et d'orientation vers spécialiste (nutritionniste, psychologue...)",
    "Je n'ai pas d'attentes particulières, je suis satisfait de mon suivi "])
    orientatio=st.text_input("10.Vers quel type de spécialiste souhaiteriez-vous être orienté dans le cadre de votre suivi santé au travail ? ")
    constat_prischg=st.selectbox("11.Constatez-vous une amélioration dans la prise en charge depuis votre dernière visite ? ",
    ["","Oui","Non"])
    if constat_prischg=="Oui":
        jsutification_prischg=st.text_input("12.Si oui, laquelle ?")
    else:
        jsutification_prischg=st.text_input("12.Si non, pourquoi ?")    
    comment = st.text_area("Votre avis nous intéresse:")





if st.button("Soumettre"):
    if not adresse_mail:
        st.warning("Address mail non renseigne")
    else: 
        match=  re.match(r'[^@]+@[^@]+\.[^@]+', adresse_mail)
        if match:

            # Connexion à la base de données
            conn = sqlite3.connect('feedback1.db')
            c = conn.cursor()

            # Insertion des données dans la table feedback
            c.execute("INSERT INTO feedback1 (adresse_mail,lieu_viste,satisfaction,satisfaction_generale,previsite,space_pre,question_realisa,Vous_avez_vu,votre_att,orientatio,constat_prischg,jsutification_prischg,comment) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (adresse_mail,lieu_viste,satisfaction,satisfaction_generale,previsite,space_pre,question_realisa,
        Vous_avez_vu,votre_att,orientatio,constat_prischg,jsutification_prischg,comment))

            # Enregistrement des modifications et fermeture de la connexion
            conn.commit()
            conn.close()

            st.success("Merci pour votre avis!")
        else :
           st.warning("Addresse mail invalid")
