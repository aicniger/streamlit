import streamlit as st
import pandas as pd
from transformers import pipeline, AutoTokenizer,AutoModelForSequenceClassification
import time

# Charger les données en utilisant pandas
#data = pd.read_csv("employee_comments.csv")

# Entraîner le modèle Flaubert
token=AutoTokenizer.from_pretrained("flaubert/flaubert_small_cased")
model=AutoModelForSequenceClassification.from_pretrained("nlptown/flaubert_small_cased_sentiment")
classification_pipeline = pipeline(task="sentiment-analysis", model = model,tokenizer=token)

# Définir une fonction pour effectuer l'analyse de sentiments
def sentiment_analysis(model, text):
    sentiment = classification_pipeline(text)[0]["label"]
    return sentiment

# Écrire l'interface utilisateur avec Streamlit
st.title("Auteur A.aziz IDRISSA C.")
st.write("#  Analyse de sentiments")
pharse=" Découvrez mon application Streamlit pour l'analyse de sentiment ! Obtenez des insights précieux sur vos textes en un instant. Que ce soit pour évaluer des commentaires, des avis produits ou des tweets, cette application vous fournit une analyse de sentiment rapide et fiable. Essayez-la dès maintenant et explorez le pouvoir de l'analyse des sentiments ! "
st.markdown(phrase)

# Ajouter un champ de saisie pour le commentaire de l'utilisateur
user_input = st.text_area("Soumettez votre commentaire :")
user_input=user_input.lower()
# Ajouter un bouton pour soumettre le commentaire pour l'analyse
if st.button("Analyser"):
    if not user_input:
        st.info("La cellule de commentaire est vide")
        st.stop()
    else:
        sentiment = sentiment_analysis(model, user_input)
        st.write("Le sentiment de votre commentaire est :", sentiment)







