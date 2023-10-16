import streamlit as st
import pandas as pd
import numpy as np

# Charger les DataFrames à partir de fichiers Parquet
@st.cache()
def load_data():
    try:
        df1 = pd.read_parquet("df_int.parquet")
        df2 = pd.read_parquet("df_merge.parquet")

        # Effectuer une jointure entre les DataFrames
        result = pd.merge(df1, df2, on="code_commune", how="inner")
        return result
    except FileNotFoundError:
        st.error("Le fichier de données n'a pas été trouvé.")
        return None

# Fonction pour afficher les médecins
def display_medecins(medecins):
    if not medecins.empty:
        # Trier les médecins par la variable "Distance_km"
        medecins = medecins.sort_values(by='Distance_km')

        Resultat = medecins.rename(columns={'Specialite': 'Civilite'})
        Resultat = Resultat[['Numéro', 'Civilite', 'Nom_Ps', 'Prenom_Ps', 'Commune1', 'Commune2', 'code_commune', 'Distance_km']]
        Resultat['Distance_km'] = Resultat['Distance_km'].round(1)

        st.write("Résultats :")
        st.dataframe(Resultat, height=800, width=800)
    else:
        st.warning(f"Aucun {specialite} n'a été trouvé dans la commune {nom_commune}.")

        # Demander à l'utilisateur s'il souhaite afficher les médecins des autres communes avec la même spécialité
        afficher_autres_communes = st.sidebar.radio("Afficher les professionnels des autres communes avec la même spécialité ?", ["Non", "Oui"], index=1)

        if afficher_autres_communes == "Oui":
            # Filtrer les médecins des autres communes avec la même spécialité
            autres_communes_same_specialite = df[(df['Specialite'] == specialite) & (df['Commune2_Code_Departement2'] == nom_commune)]
            autres_communes_same_specialite = autres_communes_same_specialite.sort_values(by='Distance_km')
            autres_communes_same_specialite['Distance_km'] = autres_communes_same_specialite['Distance_km'].round(1)

            st.write("Professionnels de la même spécialité dans d'autres communes triés par distance :")
            st.dataframe(autres_communes_same_specialite, height=800, width=800)

# Interface utilisateur Streamlit
st.title("Recherche de Professionnel(s) de Santé par Commune et Spécialité")

# Chargement des données
st.text("Chargement des données en cours...")
df = load_data()

if df is not None:
    # Demander à l'utilisateur de sélectionner une commune et une spécialité
    nom_commune = st.sidebar.selectbox("Sélectionnez une commune :", df['Commune1_Code_Departement1'].unique())
    specialite = st.sidebar.selectbox("Sélectionnez la spécialité :", df['Specialite'].unique())

    if st.sidebar.button("Rechercher"):
        # Filtrer les médecins en fonction de la commune et de la spécialité
        medecins = df[(df['Commune1_Code_Departement1'] == nom_commune) & (df['Specialite'] == specialite)]
        display_medecins(medecins)

