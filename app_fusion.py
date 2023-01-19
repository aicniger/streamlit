import pandas as pd
import streamlit as st
import smtplib




def main():
    st.title("Bienvenuue Chez Santra Plus")
    st.write("# Vous êtes sur la plateforme de fusion des bases de données pour les envois des emails concernant le questionnaire de satisfaction de Santra plus")

    st.markdown('''
        Il s'agit d'une plateforme qui va notre permettre de faire une fusion automatique de la table des salaires hors consultation spécialise* et la table des salaires vus la semaine précédente(deux jours) pour les envoyer des mails automatiquement juste après la fusion
         ''')
    st.header('')


    # Ajout d'un widget pour charger les deux fichiers de données
    file1 = st.file_uploader("Data consultation spécialise:", type=["xlsx"])
    file2 = st.file_uploader("Data Activité de la semaine:", type=["xlsx"])

    if file1 and file2:
        # Charger les fichiers de données en utilisant pandas
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        # Reduction de colonne
        df2=df2[["matricule_personne","email"]]
        df1=df1[["matricule_personne","nom","prenom"]]

        # Définir une clé commune pour fusionner les deux fichiers
        #key = st.text_input("Enter the key column to merge on:")
        key="matricule_personne"
        
        # Fusionner les deux fichiers en utilisant la fonction merge()
        merged_data = pd.merge(df1, df2, on=key)
        #merged_data=merged_data.loc[merged_data["email"]!="<NA>"]
        merged_data=merged_data.dropna()

        # affichage du résultat de fusion
        st.write(" **Table issue de la fusion de deux tables importes précedement**")
        st.dataframe(merged_data)
        
        # Ajout d'un bouton pour exporter les données fusionnées vers un nouveau fichier
        if st.button('Export votre table'):
            st.markdown('Exporting data...')
            merged_data.to_excel('merged_data.xlsx', index=False)
            st.success('Data exported successfully.')
        # Sélectionner la colonne contenant les adresses e-mail
        email_column = st.selectbox('Select the email column:', merged_data.columns.tolist())
        emails = merged_data[email_column].tolist()

        #Définir les paramètres de connexion au serveur SMTP
        smtp_server = st.text_input('SMTP server:', 'smtp.example.com')
        smtp_port = st.number_input('SMTP port:', value=587)
        username = st.text_input('Adresse E-mail De Santra Plus:')
        password = st.text_input('Password:',type='password')
        # Définir le contenu du message
        subject = st.text_input("Objet:", "Email de test")
        body_html ="""
        <html>
            <head>
            </head>
            <body>
                </p>
                Bonjour,
                </p>
               <p> Ceci est un message de test envoyé à partir d'un script Python. vous pouvez clic sur le <a href="https://forms.office.com/Pages/ResponsePage.aspx?id=xo6bsDU0UEa-VHW_vZm-AM2EGlgeVthGoF6CJ9amidZUQTRJWjIwQzlOM09CRFFOUDdWUjc4Rk03RCQlQCN0PWcu">lien</a> 
                        pour repondre à notre questionnaire de satisfaction suite à votre visité chez nous.
                </p>
                </p>
                </p>
                Bien à vous,
                Aziz.
                </p>
                <img src="https://www.linkedin.com/company/santra-plus/mycompany/"> 
                </p>
            </body>
        </html>
        """

        if st.button('Envoye'):
            try:
                #Créer une connexion SMTP
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(username, password)
            except:
                st.error("impossible de se connecter au serveur")
                
            #Envoyer le message à toutes les adresses e-mail
            try:
                for email in to_emails:
                    msg = MIMEText(body_html, 'html')
                    msg['Subject'] = subject
                    msg['From'] = username
                    msg['To'] = email
                    server.sendmail(username, email, msg.as_string())
                st.success("Messages sent successfully.")
            except:
                st.error("impossible d'envoyer les mails")
            finally:
                #Fermer la connexion SMTP
                server.quit()
        


if __name__ == '__main__':
    main()



