import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import plotly.graph_objects as go
import base64
from io import BytesIO
import streamlit.components.v1 as components
etoiles = components.declare_component("etoiles", path="./front")



def main():
   
    st.set_page_config(
    page_title="Bienvenuue Chez Santra Plus",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
    st.title("Bienvenue Chez Santra Plus")

    data=pd.read_excel("Questionnaire de satisfaction.xlsx")
    
    mise_jour=st.sidebar.checkbox('Voulez-vous faire une mise à jour manuellement ?')
    if mise_jour:
        uploaded_file = st.sidebar.file_uploader("Questionnaire de satisfaction:", type=["xlsx"])
        df_brut=uploaded_file
    
    data["Date"]=pd.to_datetime(data["Heure de début"]).dt.date
    data_brut=data
    date = data.Date.tolist()
   
    a=list(data["Où avez-vous passé votre visite ?"].dropna().unique())
    #a
    h=data[data["Où avez-vous passé votre visite ?"]==a[1]]
    #h.shape
    index=list(data["Où avez-vous passé votre visite ?"].dropna().unique())+["Santra Plus"]
    index=index.index("Santra Plus")
    centre=st.sidebar.selectbox("Sélectionner le centre ", list(data["Où avez-vous passé votre visite ?"].dropna().unique())+["Santra Plus"],index=index,disabled=False)
    if centre==a[0]:
        data=data_brut.loc[data_brut["Où avez-vous passé votre visite ?"]==a[0]]

    elif centre=="Santra Plus": data=data_brut

    else : 
        data=data_brut.loc[data_brut["Où avez-vous passé votre visite ?"]==a[1]]    
    
    date_debut = st.sidebar.date_input("Date début", min(date),min_value=min(date), max_value=max(date))
    date_fin = st.sidebar.date_input("Date fin", max(date),min_value=date_debut, max_value=max(date))
    if date_debut and date_fin:
        
        data=data.loc[(data["Date"]>=date_debut) & (data["Date"]<=date_fin) ]
        #df_senti=data[data["Où avez-vous passé votre visite ?"]==a[0]]
        df_senti=data
        df_senti=df_senti.loc[:,"Votre avis nous intéresse :"]
        df_senti=df_senti.dropna()
        df_senti=df_senti.to_list()
        #df_senti

        liste=[]
        token=AutoTokenizer.from_pretrained("flaubert/flaubert_small_cased")
        model=AutoModelForSequenceClassification.from_pretrained("nlptown/flaubert_small_cased_sentiment")
        classification_pipeline = pipeline(task="sentiment-analysis", model = model,tokenizer=token)
        df1=pd.DataFrame()
        # commentaires=["J'ai eu l'impression d'être reçu par un médecin qui en avait totalement rien à faire... L'impression que ma demande n'était pas prise au sérieux.",
        #     "Le côté humain qui est un peu délaissé avec la tablette Le côté grosse usine avec tout ses box. Ainsi que certains médecins qui ne disent pas bonjour aux autres patients lorsqu'ils viennent chercher le leur.",
        #     "Équipe accueillent et efficace dans son domaine !  Merci pour votre disponibilité et votre écoute ! "]
        if __name__=="__main__":
            for sentiemnt in classification_pipeline(df_senti):
                #print(f"\n{sentiemnt}")
                liste.append(sentiemnt)   
                #df1= pd.DataFrame.from_dict(sentiemnt)   
            #df=pd.read_excel("Questionnaire de satisfaction suite à votre visite (2) 2.xlsx")
            
            df=data.loc[:,"Votre avis nous intéresse :"]
            df_copy=df.dropna()
            df_copy=pd.DataFrame(df_copy).reset_index()
            #df_copy.loc[1,"Votre avis nous intéresse :"]
            #liste
            df1=pd.DataFrame(liste)
            df1["Avis_reçu"]=df_copy["Votre avis nous intéresse :"]
            
    

        colors = {
        "very_positive": "#bf230f",
        "mixed": "#d94f3d",
        "negative": "#8c2d20",
        "very_negative": "#8c2d20",
        "positive": "#19848c" 
    }
        df_colore = pd.DataFrame([colors], index=["colors"]).T
        colors = [ "red", 'gold','lightgreen']

        # pull is given as a fraction of the pie radius
        fig1 = go.Figure(data=[go.Pie(labels=df1.label, values=df1.index, pull=[0, 0, 0.1, 0])])
        #fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        fig1.update_traces(hoverinfo='label+percent', textinfo='label+percent',  textfont_size=15,
                marker=dict(colors=colors, line=dict(color='#000000', width=4)))
        #fig.update_layout(
        #annotations=[dict(text="", x=0.5, y=1, font_size=20, showarrow=True)])
        fig1.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="Répartition des avis de salariés suite à leurs visites", x=0.2, y=1, font_size=15), width=500, height=500,
        showlegend=False)
        #st.plotly_chart(fig1)

        
        df2=data
        #c=df2["Qu'attendez vous de votre service de santé au travail ?"].value_counts().reset_index()
        #c=c.loc[c["Qu'attendez vous de votre service de santé au travail ?"]>2]

        # f=data["Où avez-vous passé votre visite ?"].value_counts().reset_index()
        # f.loc[f["index"]=="Gonfreville L'orcher\xa0", "precent"]=round(f["Où avez-vous passé votre visite ?"][0]/(sum(f["Où avez-vous passé votre visite ?"])),2)
        # f.loc[f["index"]!="Gonfreville L'orcher\xa0", "precent"]=round((1-(f["Où avez-vous passé votre visite ?"][0]/(f["Où avez-vous passé votre visite ?"][0]+f["Où avez-vous passé votre visite ?"][1]))),2)

        
    


    #################### Pie Chart Logic ##################################

        wine_cnt = df2
        a=df2["Etes-vous satisfait de l'accueil de manière générale ?"].value_counts().reset_index()
        a["Note"]=a["index"]
        a=a.drop(["index"],axis=1)
        pie_fig=px.pie(a,labels="Note", values="Etes-vous satisfait de l'accueil de manière générale ?",color_discrete_sequence=px.colors.sequential.RdBu)
        pie_fig.update_layout(legend_traceorder="reversed")
        pie_fig.update_traces(hoverinfo='label+percent', textinfo='label+percent',  textfont_size=15,
                marker=dict(colors=colors, line=dict(color='#000000', width=4)))
        pie_fig.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="Etes-vous satisfait de l'accueil de manière générale", x=0.2, y=1, font_size=20), width=500, height=500,
        showlegend=True)

        #fig_his=px.histogram(f,x="index",y="precent")

        b=df2["Etes vous globalement satisfait de votre visite ?"].value_counts().reset_index()
        b["Note"]=b.iloc[:,0]
        b.loc[b["Note"]==10, "note_recu"]="10/10"
        b.loc[b["Note"]==9, "note_recu"]="9/10"
        b.loc[b["Note"]==8, "note_recu"]="8/10"
        b.loc[b["Note"]==7, "note_recu"]="7/10"
        b.loc[b["Note"]==6, "note_recu"]="6/10"
        b.loc[b["Note"]==4, "note_recu"]="5/10"
        b.loc[b["Note"]==3, "note_recu"]="3/10"
        b.loc[b["Note"]==2, "note_recu"]="2/10"
        b.loc[b["Note"]==1, "note_recu"]="1/10"
        b.loc[b["Note"]==0, "note_recu"]="0/10"
        pie_fig2=px.histogram(b,x="Etes vous globalement satisfait de votre visite ?",y="note_recu",text_auto=True,title='Etes vous globalement satisfait de votre visite')

        k=data["Etes vous globalement satisfait de votre échange avec le professionnel de santé ?"].value_counts().reset_index()
        k["note_recu"]=k["index"].astype("int")
        k.loc[k["note_recu"]==10, "Note_recu"]="10/10"
        k.loc[k["note_recu"]==9, "Note_recu"]="9/10"
        k.loc[k["note_recu"]==8, "Note_recu"]="8/10"
        k.loc[k["note_recu"]==7, "Note_recu"]="7/10"
        k.loc[k["note_recu"]==6, "Note_recu"]="6/10"
        k.loc[k["note_recu"]==5, "Note_recu"]="5/10"
        k.loc[k["note_recu"]==4, "Note_recu"]="4/10"
        k.loc[k["note_recu"]==3, "Note_recu"]="3/10"
        k.loc[k["note_recu"]==2, "Note_recu"]="2/10"
        k.loc[k["note_recu"]==1, "Note_recu"]="1/10"
        k.loc[k["note_recu"]==0, "Note_recu"]="0/10"
        pie_fig3=px.histogram(k,x="Etes vous globalement satisfait de votre échange avec le professionnel de santé ?",y="Note_recu",text_auto=True,title='Etes vous globalement satisfait de votre échange avec le professionnel de santé')
        pie_fig3=px.pie(k,values="Etes vous globalement satisfait de votre échange avec le professionnel de santé ?",labels="Note_recu")
        pie_fig3.update_traces(hoverinfo='label+percent', textinfo='label+percent',  textfont_size=15,
                marker=dict(colors=colors, line=dict(color='#000000', width=4)))
        pie_fig3.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="Etes vous globalement satisfait de votre échange avec le professionnel de santé", x=0.2, y=1, font_size=20), width=600, height=550,
        showlegend=True)

        #
        # pull is given as a fraction of the pie radius
        pie_fig = go.Figure(data=[go.Pie(labels=a["Note"], values=a["Etes-vous satisfait de l'accueil de manière générale ?"], pull=[0, 0, 0.1, 0])])
        #fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        pie_fig.update_traces(hoverinfo='label+percent', textinfo='label+percent',  textfont_size=15,
                marker=dict(colors=colors, line=dict(color='#000000', width=4)))
        #fig.update_layout(
        #annotations=[dict(text="", x=0.5, y=1, font_size=20, showarrow=True)])
        pie_fig.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="Etes-vous satisfait de l'accueil de manière générale ", x=0.2, y=1, font_size=15), width=600, height=550,
        showlegend=False)


        #
        
        go_fig=go.Figure()
        go_fig.add_trace(go.Pie(labels=k["Etes vous globalement satisfait de votre échange avec le professionnel de santé ?"], values=k['index']))
        go_fig.update_traces(hoverinfo='label+percent', textinfo='label+percent',  textfont_size=15,
                marker=dict(colors=colors, line=dict(color='#000000', width=4)))
        #fig.update_layout(
        #annotations=[dict(text="", x=0.5, y=1, font_size=20, showarrow=True)])
        go_fig.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="Etes vous globalement satisfait de votre échange avec le professionnel de santé", x=0.8, y=1, font_size=15), width=500, height=500,
        showlegend=False)
        go_fig=px.bar(k,x="Etes vous globalement satisfait de votre échange avec le professionnel de santé ?",y="Note_recu",text_auto=True,title="Etes vous globalement satisfait de votre échange avec le professionnel de santé")
        g=data["Qu'attendez vous de votre service de santé au travail ?"].value_counts().reset_index()
        g=g.loc[0:4,["index","Qu'attendez vous de votre service de santé au travail ?"]]
        g_ig=px.histogram(g,y="index",x="Qu'attendez vous de votre service de santé au travail ?",text_auto=True)
        # TOP KPI's
        total_sales = int(data["ID"].count())
        average_rating = round(data["Etes-vous satisfait de l'accueil de manière générale ?"].mean(), 2)
        #p=int(round(average_rating, 0))
        #star_rating=etoiles(value=p)
        
        star_rating = ":star:" * int(round(average_rating, 0))
        average_sale_by_transaction = round(data["ID"].mean(), 2)

        note_pro = round(data["Etes vous globalement satisfait de votre échange avec le professionnel de santé ?"].mean(), 2)
        star_rating_note_pro = ":star:" * int(round(note_pro, 0))

        note_glo = round(data["Etes vous globalement satisfait de votre visite ?"].mean(), 2)
        star_rating_note_glo = ":star:" * int(round(note_glo, 0))
        

        nb_sal_column, note_moy_acul_column, note_moy_prof_column,note_moy_glo_column = st.columns(4)
        with nb_sal_column:
            st.subheader("Nombres de salariés :")
            st.subheader(f" {total_sales:,} Personnes")
        with note_moy_acul_column:
            st.subheader("Note Moyenne pour l'accueil:")
            st.subheader(f"{average_rating} {star_rating}")
        with note_moy_prof_column:
            st.subheader("Note Moyenne pour les professionnels :")
            #st.subheader(etoiles(5))
            #st.subheader(f"{note_pro} {star_rating_note_pro}")
            st.subheader(f"{note_pro}")
        with note_moy_glo_column:
            st.subheader("Note Moyenne globale satisfaction visite :")
            #st.subheader(etoiles(5))
            #st.subheader(f"{note_glo} {star_rating_note_glo}")   
            st.subheader(f"{note_glo}") 

        container1 = st.container()
        col1, col2 = st.columns(2)

        with container1:
            with col1:
                
                pie_fig
            with col2:
                go_fig


        container2 = st.container()
        col3, col4 = st.columns(2)

        with container2:
            with col3:
                fig1
            with col4:
                pie_fig2

        effectif=df2["Avez-vous passé une pré-visite sur tablette ?"].value_counts().reset_index()
        bbb=effectif.iloc[0,1] 
        st.write("Nombres de salariés qui ont passé une pré-visite sur tablette :",f" {bbb:,} Personnes")
        
        

        
        assistant=df2["Disponibilité de l'assistante"].value_counts().reset_index()  
        assistant["Disponibilité de l'assistante"]=assistant["Disponibilité de l'assistante"]/effectif.iloc[0,1]
        assistant["Disponibilité de l'assistante"]=round(assistant["Disponibilité de l'assistante"],2)
        delai=df2.iloc[:,10].value_counts().reset_index()
        delai.iloc[:,1]=delai.iloc[:,1]/effectif.iloc[0,1] 
        delai.iloc[:,1]=round(delai.iloc[:,1],2)
        comprehension=df2.iloc[:,11].value_counts().reset_index()
        comprehension.iloc[:,1]=comprehension.iloc[:,1]/effectif.iloc[0,1] 
        comprehension.iloc[:,1]=round(comprehension.iloc[:,1],2)
        confident=df2.iloc[:,12].value_counts().reset_index()
        confident.iloc[:,1]=confident.iloc[:,1]/effectif.iloc[0,1] 
        confident.iloc[:,1]=round(confident.iloc[:,1],2)
        materiel=df2.iloc[:,13].value_counts().reset_index()
        materiel.iloc[:,1]=materiel.iloc[:,1]/effectif.iloc[0,1]
        materiel.iloc[:,1]=round(materiel.iloc[:,1],2)
        #df2.columns
        
        #his=px.histogram(k,x="Etes vous globalement satisfait de votre échange avec le professionnel de santé ?",y="Note_recu",text_auto=True,title='Etes vous globalement satisfait de votre échange avec le professionnel de santé')
    
        container3 = st.container()
        col5,col6,col7,col8,col9 = st.columns(5)

        with container3:
           with col5:
                assistant 
           with col6:
                delai  
           with col7:
                comprehension 
           with col8:
               confident
           with col9:
                materiel

        
        
        
        
    # Ajout d'un bouton pour exporter les données (les mails de salariés qui ont donné un trés bon avis) vers un nouveau fichier
        st.write(" Voici votre liste de reponses vous pouvez l'exporter si nécessaire :")
        choix=st.sidebar.selectbox("**Vous voulez voir la liste de reponses**",["","Positive","Négative"])
        if choix=="":
            st.markdown("**Veuillez selectionner le type de liste parmi les deux proposées dans la barre latérale pour voir une table de reponses**")
        else :    
            if choix=="Positive":
                df_mails=data.loc[:,["Votre adresse mail","Votre avis nous intéresse :"]]
                df_mails=df_mails.dropna()
                df_mails=df_mails.reset_index()
                df_mails=df_mails.drop(["index"],axis=1)
                df_fin=pd.concat([df1,df_mails],axis=1)
                df_fin=df_fin.loc[:,["Votre adresse mail","label","score","Avis_reçu"]]
                df_print=df_fin.loc[(df_fin["label"]=="very_positive" ) & (df_fin["score"]>0.1)]

                # df_mails=data["Votre adresse mail"].dropna()
                # df1=pd.DataFrame(liste)
                # df1["Mails"]=df_mails
                # df_print=df1.loc[(df1["label"]=="very_positive") & (df1["score"]>0.5)]
                st.dataframe(df_print)
                if st.button('Télécharger la liste de réponses positives'):
                    st.markdown('Downloading data...')
                    buf = BytesIO()
                    df_print.to_excel(buf, index=False, engine='xlsxwriter')
                    buf.seek(0)
                    b64 = base64.b64encode(buf.read()).decode()
                    file_size = buf.tell()
                    st.write("Size of the file : ", round(file_size/(1024*1024), 2),"MB")
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    href = f'<a href="data:application/vnd.ms-excel;base64,{b64}" download="merged_data.xlsx">Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True)
                        
            
            else :
        # Ajout d'un bouton pour exporter les données (les mails de salariés qui ont donné un trés mouvais avis) vers un nouveau fichier
                

                df_mails=data.loc[:,["Votre adresse mail","Votre avis nous intéresse :"]]
                df_mails=df_mails.dropna()
                df_mails=df_mails.reset_index()
                df_mails=df_mails.drop(["index"],axis=1)
                df_fin=pd.concat([df1,df_mails],axis=1)
                df_fin=df_fin.loc[:,["Votre adresse mail","label","score","Avis_reçu"]]
                df_print2=df_fin.loc[((df_fin["label"]=="very_negative") | (df_fin["label"]=="negative") ) & (df_fin["score"]>0.1)]
                st.dataframe(df_print2)
                if st.button('Télécharger la liste de réponses négatives'):
                    st.markdown('Downloading data...')
                    buf = BytesIO()
                    df_print2.to_excel(buf, index=False, engine='xlsxwriter')
                    buf.seek(0)
                    b64 = base64.b64encode(buf.read()).decode()
                    file_size = buf.tell()
                    st.write("Size of the file : ", round(file_size/(1024*1024), 2),"MB")
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    href = f'<a href="data:application/vnd.ms-excel;base64,{b64}" download="merged_data.xlsx">Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True) 







   
if __name__ == '__main__':
    main()
