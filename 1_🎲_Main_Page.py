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
        page_title='Main Page',
        page_icon='🎲',
        layout='wide',)
    

# ===========================================================================
#Funções 
#==========================================================================

#Função visualização do Mapa 

def mapa_dos_restaurantes(df2):
    mapa = df2.loc[:, ['restaurant_name', 'average_cost_for_two', 'currency', 'aggregate_rating', 'country', 'city', 'cuisines', 'latitude', 'longitude', 'rating_color']]
    map = folium.Map(location=[0, 0], zoom_start=1)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map)
    
    color_mapping = {
    "darkgreen": ["4.0", "4.5"],
    "green": ["4.5", "5.0"],
    "lightgreen": ["3.5", "4.0"],
    "orange": ["2.9", "3.5"],
    "red": ["2.0", "2.8"],
    "darkred": ["0.0", "2.0"]
}
    for index, location in mapa.iterrows():
    
        # Obter a cor atribuída
        assigned_color = location['rating_color']
        
        # Obter a classificação real
        real_rating = location['aggregate_rating']
        
        # Verificar em qual faixa de avaliação a classificação se enquadra
        for color, rating_range in color_mapping.items():
            min_range = float(rating_range[0])
            max_range = float(rating_range[1])
            
            if min_range <= real_rating <= max_range:
                assigned_color = color
                break
        
        folium.Marker([location['latitude'], location['longitude']],
                      popup=folium.Popup(f'''<h6><b>{location['restaurant_name']}</b></h6>
                      <h6>Preço: {location['average_cost_for_two']} ({location['currency']}) para dois <br>
                      Culinária: {location['cuisines']} <br>
                      Avaliação: {location['aggregate_rating']}/5.0</h6>''',
                      max_width=300, min_width=150),
                      tooltip=location['restaurant_name'],
                      icon=folium.Icon(color=assigned_color, icon='home', prefix='fa')).add_to(marker_cluster)
    
    folium_static(map, width=1024, height=600)
# ---------------------------------------------------------------------------------------------------------------------------
# --------------------- Início da Estrutura Lógica do Código ---------------
# ===========================================================================
#Importar os dados
#==========================================================================
df = pd.read_csv('dataset/zomato_tratado.csv')
df1 = df.copy()
df2 = df.copy()
# ===========================================================================
#Barra lateral
#==========================================================================
image = Image.open( 'logo.png' )
st.sidebar.image(image)

st.sidebar.markdown('<h1 style="color: #f72585;">Filtros</h2>', unsafe_allow_html=True)

country = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']
country_op = st.sidebar.multiselect('Escolha os Países que deseja visualizar as informações',
                                   country,
                                   default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'] )

#Filtro de cidades 
df2 = df2.loc[df2['country'].isin(country_op),:]

# download dos dados Tratados 
st.sidebar.markdown('### Dados Tratados')
dados =pd.read_csv('dataset/zomato_tratado.csv')
st.sidebar.download_button(
    label='Download',
    data=dados.to_csv(index=False, sep=";"),
    file_name="data_fome.csv",
    mime="text/csv",)

# Colocar o button para download dos dados tratados 
#Quem desenvolveu a pagina.
st.sidebar.markdown('### Powered by Elio Matheus')
# ===========================================================================
#Layout no Streamlit
#==========================================================================
st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!' )

# Container dividido em 5 colunas 
with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:' )
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        unico = len(df1.loc[:,'restaurant_id'].unique())
        col1.metric('Restaurantes Cadastrados', unico)
        
    with col2:
        unico = len(df1.loc[:,'country'].unique())
        col2.metric('Países Cadastrados', unico)
        
    with col3:
        unico = len(df1.loc[:,'city'].unique())
        col3.metric('Cidades Cadastradas', unico)
        
    with col4:
        total_votes = df1['votes'].sum()
        total_votes = f'{total_votes:,.0f}'
        total_votes = total_votes.replace(',','.')
        col4.metric('Avaliações Feitas na Plataforma', total_votes)
        
    with col5:
        unico = len(df1.loc[:,'cuisines'].unique())
        col5.metric('Tipos de Culinárias Oferecidas', unico)
        

with st.container():
    mapa_dos_restaurantes(df2)