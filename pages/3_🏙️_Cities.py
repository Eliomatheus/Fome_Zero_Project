#Bibiliotecas
from plotly import colors
import pandas as pd
import re
import numpy as np
import inflection
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import folium
from streamlit_folium import folium_static
from haversine import haversine


st.set_page_config(
        page_title='Cities',
        page_icon='🏙️',
        layout='wide',)
    

# ===========================================================================
#Função de inicialização para limpeza do dataframe
#==========================================================================
#-------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
# --------------------- Início da Estrutura Lógica do Código ---------------
# ===========================================================================
#Importar os dados
#==========================================================================
df = pd.read_csv('dataset/zomato_tratado.csv')
df1 = df.copy()

#Barra lateral
#==========================================================================
image = Image.open( 'logo.png' )
st.sidebar.image(image)

st.sidebar.markdown('<h1 style="color: #f72585;">Filtros</h2>', unsafe_allow_html=True)

country = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']
country_op = st.sidebar.multiselect(' Escolha os Países que deseja visualizar as informações',
                                   country,
                                   default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'] )

#Filtro de cidades 
df1 = df1.loc[df1['country'].isin(country_op),:]

# Filtro de Qauntidade 
barra = st.sidebar.slider("Qauntidade de Cidades:", min_value=5, max_value=18, value=10)

#Quem desenvolveu a pagina.
st.sidebar.markdown('### Powered by Elio Matheus')


#--------------------------------------------------------------------------------
#Layout no Streamlit 
#--------------------------------------------------------------------------------
st.markdown( '# 🌎 Visão Cidades' )

with st.container():
    st.markdown('## Visão Cidades')
    st.markdown('### Top {} cidades com mais restaurantes na base de dados'.format(barra))
    top_rest = df1.groupby(['city', 'country']).count().sort_values(by='restaurant_id', ascending=False).reset_index().head(barra)
    fig = px.bar(top_rest.head(barra), x= 'city', y='restaurant_id', text_auto=True, labels={'city': 'Nome da Cidade', 'restaurant_id': 'Quantidade de Restaurantes', 'country': 'Pais'},
                 color='country',
                 title='Top {} cidades com mais restaurantes na base de dados'.format(barra))

    st.plotly_chart(fig,use_container_width=True,theme=None)

    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        max_med = df1.loc[:,['country','city','aggregate_rating','restaurant_id']].groupby(['country','city','restaurant_id']).mean().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
        max_med = max_med.loc[max_med['aggregate_rating'] >= 4,['country','city','restaurant_id']].groupby(['country','city']).count().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index() 

        fig = px.bar(max_med.head(barra), x='city', y='restaurant_id', text_auto=True, labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes', 'country': 'País'},
                     color='country',
                     title='Top {} Cidades com Restaurantes com média de avaliação acima de 4'.format(barra))
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:
        min_med = df1.loc[:,['country','city','aggregate_rating','restaurant_id']].groupby(['country','city','restaurant_id']).mean().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
        min_med = min_med.loc[min_med['aggregate_rating'] <= 2.5,['country','city','restaurant_id']].groupby(['country','city']).count().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index() 


        fig = px.bar(min_med.head(barra), x='city', y='restaurant_id', text_auto=True, labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes', 'country': 'País'},
                     color='country',
                     title='Top {} Cidades com Restaurantes com média de avaliação abaixo de 2.5 '.format(barra))
        st.plotly_chart(fig, use_container_width=True, theme=None) 


with st.container():
    
    top_type = df1.loc[:,['country','city','cuisines','restaurant_id']].groupby(['country','city','cuisines']).count().sort_values(by=['restaurant_id'],ascending=[False]).reset_index()
    top_type = top_type.loc[:,['country','city','cuisines']].groupby(['country','city']).count().sort_values(by=['cuisines','city','country'],ascending=[False,True,True]).reset_index()
    
    
    fig = px.bar(top_type.head(barra), x='city', y='cuisines', text_auto=True, labels={'city':'Cidade','cuisines':'Quantidade de Tipos Culinários Únicos','country':'País'},color='country',title='Top {} Cidades mais restaurantes com tipos culinários distintos'.format(barra))
   
    st.plotly_chart(fig, use_container_width=True, theme=None)




