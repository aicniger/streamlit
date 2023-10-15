import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round
import _thread
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env


# Définir une fonction de hachage personnalisée pour _thread._local
def hash_thread_local(local_obj):
    # Vous pouvez retourner une valeur de hachage basée sur les attributs de l'objet _thread._local
    return hash(str(local_obj))


@st.cache_resource()
def load_data():
    try:
        # Créer une session Spark
        #spark = SparkSession.builder.appName("MySparkApp").getOrCreate()
        spark = SparkSession.builder.appName("MySparkApp").config("spark.jars", os.environ.get("JAVA_HOME")).getOrCreate()


        # Charger les DataFrames à partir de fichiers Parquet
        df1_df_int1 = spark.read.parquet("df_int.parquet")
        df2_df_merge = spark.read.parquet("df_merge.parquet")

        # Effectuer une jointure entre les DataFrames
        result = df1_df_int1.join(df2_df_merge, "code_commune", how="inner")
        return result
    except FileNotFoundError:
        st.error("Le fichier de données n'a pas été trouvé.")
        return None

# ...

# Chargement des données

df = load_data()

# Fonction pour afficher les médecins
def display_medecins(medecins):
    if not medecins.isEmpty():
        # Trier les médecins par la variable "Distance_km"
        medecins = medecins.orderBy('Distance_km')

        Resultat = medecins.selectExpr("0 as Numéro", "Specialite as Civilite", "2 as Nom_Ps", "3 as Prenom_Ps", 'Commune1', 'Commune2', 'code_commune', 'Distance_km')
        Resultat = Resultat.withColumn("Distance_km", round(col("Distance_km"), 1))

        st.write("Résultats :")
        st.dataframe(Resultat.toPandas(), height=800, width=800)
    else:
        st.warning(f"Aucun {specialite} n'a été trouvé dans la commune {nom_commune}.")

        # Demander à l'utilisateur s'il souhaite afficher les médecins des autres communes avec la même spécialité
        afficher_autres_communes = st.sidebar.radio("Afficher les professionnels des autres communes avec la même spécialité ?", ["Non", "Oui"], index=1)

        if afficher_autres_communes == "Oui":
            # Filtrer les médecins des autres communes avec la même spécialité
            autres_communes_same_specialite = df.filter((col("Specialite") == specialite) & (col('Commune2_Code_Departement2') == nom_commune))
            autres_communes_same_specialite = autres_communes_same_specialite.orderBy('Distance_km')
            autres_communes_same_specialite = autres_communes_same_specialite.withColumn("Distance_km", round(col("Distance_km"), 1))

            st.write("professionnel(s) de la même spécialité dans d'autres communes triés par distance :")
            st.dataframe(autres_communes_same_specialite.toPandas(), height=800, width=800)

# Interface utilisateur Streamlit
st.title("Recherche de Professionnel(s) de Santé par Commune et Spécialité")

# Chargement des données
st.text("Chargement des données en cours...")
df = load_data()

if df is not None:
    # Sélectionnez les communes uniques disponibles dans le DataFrame
    #communes_uniques = df.select("Commune1").distinct().rdd.map(lambda row: row[0]).collect()

    # Sélectionnez les spécialités uniques disponibles dans le DataFrame
    #specialites_uniques = df.select("Specialite").distinct().rdd.map(lambda row: row[0]).collect()

    # Demander à l'utilisateur de sélectionner une commune parmi les communes uniques dans la barre latérale
    nom_commune = st.sidebar.selectbox("Sélectionnez une commune :", df.select("Commune1_Code_Departement1").distinct())

    # Demander à l'utilisateur la spécialité du médecin recherché dans la barre latérale
    specialite = st.sidebar.selectbox("Sélectionnez la spécialité  :", df.select("Specialite").distinct())

    if st.sidebar.button("Rechercher"):
        # Filtrer les médecins en fonction de la commune et de la spécialité
        medecins = df.filter((col('Commune1_Code_Departement1') == nom_commune) & (col("Specialite") == specialite))
        display_medecins(medecins)
