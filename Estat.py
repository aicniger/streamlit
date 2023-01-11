
import streamlit as s
import pandas as pd
import plotly.express as px
#import mysql.connector
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from plotly.subplots import make_subplots

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM sortant"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))
# df_s = result_dataFrame

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM metier"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))
# df_m = result_dataFrame

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM secteur"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))
# df_sec = result_dataFrame

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM residence"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))
# df_r = result_dataFrame

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM commune"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))
# df_com = result_dataFrame

# try:
#     mydb = connection = mysql.connector.connect(host='localhost',
#                                                 database='base',
#                                                 user='root',
#                                                 password='')
#     query = "SELECT * FROM reponses"
#     result_dataFrame = pd.read_sql(query, mydb)
#     mydb.close()
# except Exception as e:
#     mydb.close()
#     print(str(e))


# # fusion sortant metier(id_sortant id_metier)
# dfsm = pd.merge(df_s, df_m, on='id_metier', how='left')

# # fusion dfsm er secteur(id_secteur)
# dfsm_sec = pd.merge(dfsm, df_sec, on='id_secteur', how='left')

# # fusion précédent et residence(id_residence)
# dfsm_sec_res = pd.merge(dfsm_sec, df_r, on='id_residence', how='left')

# # fusion précédent et commune(id_commune)
# dfsm_sec_res_com = pd.merge(dfsm_sec_res, df_com, on='id_commune', how='left')

# # fusion précédent et reponse(id_sortant)
# df_fin = dfsm_sec_res_com
# df = df_fin
df_resp=pd.read_csv("df_rep.csv",sep=",",decimal=".")
data=pd.read_csv("df_fin.csv",sep=",",decimal=".")
df_fin=data
df=df_fin



def main():
    s.title("Auteur Aziz")
    s.write("# Tableau de bord des sortants de formation professionelle au Niger")
    #  with s.sidebar:
    #     s.subheader('Apropos')
    #     s.markdown(
    #         'Bienvennue sur cette page vous allez retrouver des **statisques** et **graphiques**')
    # s.sidebar.image(
    #     'https://streamlit.io/images/brand/streamlit-mark-color.png', width=100)

    s.markdown('''
        Il s'agit d'un tableau de bord montrant les *Statistiques* de différents types de :Formation professionelle suivis par les sortans  
         ''')
    s.header('')

    # fonction d'import de dataset
    # affiche data
    # df = result_dataFrame
    #df_sample = df
    # s.write(df_sample)
    s.header('Statistiques récapitulatives')
    stats = df_fin.groupby('id_sortant')['sexe'].agg(
        [('nombre', 'value_counts')]).reset_index()
    stats = stats.groupby('sexe')['nombre'].agg(
        [('index', 'value_counts')]).reset_index()
    stats['aziz'] = stats['index']
    
    stat1 = df.groupby('nom_metier')[
        'id_metier'].agg([('nombre', 'value_counts')])
    stat2 = df.groupby('quartier')[
        'id_residence'].agg([('nombre', 'value_counts')])
    #s.dataframe(stats)
    #s.dataframe(stat1)
    #s.dataframe(stat2)

    # line_fig = px.line(df[df['sexe'] == 'H'],
    #                    x='date_naiss', y='id_sortant',
    #                    title='Representation')
    # s.plotly_chart(line_fig)
    fig1 = go.Figure(data=[go.Histogram(y=df["sexe"], name="count", texttemplate="%{x}", textfont_size=20)])
    
    # s.plotly_chart(fig)
    df_resp=pd.read_csv("df_rep.csv",sep=",",decimal=".")
    d=df_resp.groupby('reponse')["id_sortant"].agg([("Nombre","count")]).reset_index() 
    fig2 = px.bar(d, x='Nombre',y="reponse" ,orientation='h')
    fig2=go.Figure(go.Bar(
            x=d["Nombre"],
            y=d["reponse"],
            orientation='h',textposition='inside'))
    
              
    # s.plotly_chart(fig)

    tab1, tab2 = s.tabs(["les nombres des hommes et femmes",
                         "les nombres des responses des sortans"])
    with tab1:
        s.plotly_chart(fig1, theme="streamlit", use_conatiner_width=True)
    with tab2:
        s.plotly_chart(fig2, theme=None, use_conatiner_width=True)

    a = pd.DataFrame(df["situation_pro"].value_counts().reset_index())
    b = pd.DataFrame(df["quartier"].value_counts().reset_index())
    lst = list(df.groupby('quartier'))
    colors = ['#8BC34A','#D4E157','#FFB300','#FF7043']
    # here we want our grid to be 2 x 3
    rows = 2
    cols = 3
    # continents are the first element in l
    subplot_titles = [l[0] for l in lst]

    stats = df_fin.groupby('id_sortant')['sexe'].agg(
        [('nombre', 'value_counts')]).reset_index()
    stats = stats.groupby('sexe')['nombre'].agg(
        [('index', 'value_counts')]).reset_index()
    # a compact and general version of what you did
    # specs = [[{'type':'domain'}]* cols] * rows
    
    specs = [[{"type": "pie"}, {"type": "bar"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]]
    fig = make_subplots(
        rows=rows,
        cols=cols,
        
        subplot_titles=("Situation professionelle des sortants", "",
        "Secteur de travaille des sortants", "Sortants en fonction du quartier","","Répartion des reponses des sortans"),
        specs=specs,
        print_grid=True)


    fig.add_trace(go.Pie(labels=a.loc[:, 'index'], values=a.loc[:, 'situation_pro'],
                        hole = .4,marker=dict(colors=colors),textinfo='label+value+percent',hoverinfo='label',textposition='inside'),row=1,col=1)

    d=df_resp.groupby('reponse')["id_sortant"].agg([("Nombre","count")]).reset_index()            
    fig.add_trace(go.Pie(labels=d.loc[:, 'reponse'], values=d.loc[:, 'Nombre'],
                        marker=dict(colors=colors),hovertemplate="%{label}: <br>Value: %{value} ",
                        showlegend=True,
                        textposition='inside',
                        rotation=90,hole = .4,),
                row=2,
                col=3
                )

    c=df.groupby('sexe')["nom_secteur"].agg([("Nombre","value_counts")]).reset_index()
    

    fig.add_trace(go.Pie(labels=c.loc[:, 'nom_secteur'], values=c.loc[:, 'Nombre'],
                         marker=dict(colors=colors),textinfo='label+value+percent',textposition='inside',hoverinfo='label'),
                row=1,
                col=3
                )

    #fig.add_trace(go.Bar(y=d.loc[:, 'reponse'], x=d.loc[:, 'Nombre'],orientation='h', textposition="inside",
    #            opacity=0.3, showlegend=False), row=1, col=2)

    #fig.add_trace(go.Bar(x=stats.loc[:, 'index'], y=stats.loc[:, 'sexe'],orientation='h',textposition="inside",
    #            opacity=0.3, showlegend=False), row=2, col=2)
    fig.add_trace(go.Bar(y=b.loc[:, 'quartier'], x=b.loc[:, 'index'],
                opacity=0.3, showlegend=False), row=2, col=1)

    fig.update_layout(
    #paper_bgcolor= '#FFFDE7',
    plot_bgcolor= '#FFFDE7',
    title=dict(text = "Les Graphiques",x=1,y=1,font_size=30),width=950,height=900,
    showlegend=False)
    s.plotly_chart(fig)

if __name__ == '__main__':
    main()
