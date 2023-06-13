#Bibiliotecas

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
        page_title='Countries',
        page_icon='🌎',
        layout='wide',)
    

# ===========================================================================
#Função de inicialização para limpeza do dataframe
#==========================================================================

#Criação da função de grafico de barras com cores do Azul para o vermelho
def create_bar_chart(data, x, y, xlabel, ylabel, title='', textposition='outside'):
    colorscale = [[0, '#f72585'], [0.25, '#7209b7'], [0.5, '#3a0ca3'], [0.75, '#4361ee'], [1, '#4cc9f0']]  # Paleta de cores 

    fig = px.bar(data.sort_values(y, ascending=False),
                 x=x,
                 y=y,
                 width=1000,
                 height=500,
                 labels={y: ylabel, x: xlabel},
                 text=y,
                 color=y,
                 color_continuous_scale=colorscale)
    
    fig.update_traces(textfont=dict(size=12),
                      textposition=textposition)
    
    fig.update_layout(xaxis_title_font=dict(size=16),
                      xaxis_tickfont=dict(size=10),
                      title=title)
    
    return fig

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

#Quem desenvolveu a pagina.
st.sidebar.markdown('### Powered by Elio Matheus')
#--------------------------------------------------------------------------------
#Layout no Streamlit 
#--------------------------------------------------------------------------------
st.markdown( '# 🌎 Visão Países' )

with st.container():
    
    coluna = ['restaurant_id','country']
    rest = df1.loc[:, coluna].groupby( ['country'] ).agg({'restaurant_id': 'count'}).sort_values(by='restaurant_id',
                                                                                          ascending=False).reset_index()
    fig_rest = create_bar_chart(rest, 'country', 'restaurant_id', 'País', 'Quantidade de Restaurantes',title='Qauntidade de Restaurantes Registrados por País')

    st.plotly_chart(fig_rest,use_container_width=True,theme=None)
    
    
with st.container():
    colunas = ['restaurant_id', 'country', 'city']
    city = df1.loc[:, colunas].groupby(['city', 'country']).count().sort_values(by='restaurant_id',
                                                                              ascending=False).reset_index()
    city = city.loc[:,['country','city']].groupby(['country']).count().sort_values(by='city',ascending=False).reset_index()
    
    fig_city = create_bar_chart(city, 'country','city','País','Quantidade de Cidades ',title='Qauntidade de Cidades Registrados por País')
    
    st.plotly_chart(fig_city,use_container_width=True,theme=None)
    
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        coluna = ['country', 'votes']
        avalia = round(df1.loc[:, coluna].groupby(['country']).mean().sort_values(by='votes', ascending=False).reset_index(),2)
        fig_av = create_bar_chart(avalia, 'country', 'votes','Países','Quantidade de Avaliação', title='Media de Avaliações feitas por País')
        
        st.plotly_chart(fig_av,use_container_width=True)
        
        
    with col2:
        
        coluna = ['country', 'price_in_dollar']
        prato_2 = df1.loc[:, coluna].groupby(['country']).mean().reset_index().round(2)
        fig_prato = create_bar_chart(prato_2, 'country', 'price_in_dollar', 'Países', 'Preço em Dólar', title='Média de Preço de um prato para duas pessoas por País')

        st.plotly_chart(fig_prato, use_container_width=True)





