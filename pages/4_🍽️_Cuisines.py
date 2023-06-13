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
        page_title='Cuisines',
        page_icon='🍽️',
        layout='wide',)
    

# ===========================================================================
#Função de inicialização 
def max_rating(df1,comida):
    re1 = df1.loc[(df1['cuisines'] == comida),['restaurant_name','restaurant_id','aggregate_rating']].groupby(['restaurant_name','restaurant_id']).mean().sort_values(by='aggregate_rating',ascending=False).reset_index()
    re1 = re1.loc[re1['aggregate_rating'] == re1['aggregate_rating'].max(),['restaurant_name','restaurant_id']].groupby('restaurant_name').min().sort_values(by='restaurant_id',ascending=True).reset_index()

    re1 = df1.loc[df1['restaurant_id'] == re1.iloc[0,1],['restaurant_name','country','city','average_cost_for_two','currency','cuisines','aggregate_rating']]
    
    label = f'{re1.iloc[0,5]}: {re1.iloc[0,0]}'
    value = f'{re1.iloc[0,6]}/5.0'
    ajuda = f'''País: {re1.iloc[0,1]}
        
Cidade: {re1.iloc[0,2]}
        
Média Prato para dois: {re1.iloc[0,3]} {re1.iloc[0,4]}'''
    
    return label,value,ajuda
#-----------------------------------------------------------#
def tops(df1):
    dataframe = df1.loc[df1['aggregate_rating'] == df1['aggregate_rating'].max(),['restaurant_id', 'restaurant_name', 'country', 'city','cuisines','price_in_dollar','aggregate_rating','votes']].sort_values(by='restaurant_id',ascending=True)
    dataframe['restaurant_id'] = dataframe['restaurant_id'].apply(lambda x: "{0:>20}".format(x))
    dataframe['votes'] = dataframe['votes'].apply(lambda x: "{0:>20}".format(x))
    dataframe.columns = ['ID Restaurante', 'Nome do Restaurante', 'País', 'Cidade', 'Culinária', 'Média do preço de um prato para dois em Dólar', 'Avaliação média', 'Qtde de votos']
    dataframe = dataframe.reset_index(drop=True)
    
    return dataframe
#-----------------------------------------------------------#
def grafico_1(df1,barra):
    grafico = round(df1.loc[:,['cuisines','aggregate_rating']].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=False).reset_index(),2)
    grafico = px.bar(grafico.head(barra), x='cuisines',y='aggregate_rating',text_auto=True,labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Média da Avaliação Média'},title=f'Top {barra} Melhores Tipos de Culiárias')
    return grafico
        
        
def grafico_2(df1,barra):
    grafico1 = round(df1.loc[:,['cuisines','aggregate_rating']].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=True).reset_index(),2)
    grafico1 = px.bar(grafico1.head(barra), x='cuisines',y='aggregate_rating',text_auto=True,labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Média da Avaliação Média'},title=f'Top {barra} Piores Tipos de Culiárias')
    return grafico1
    
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
barra = st.sidebar.slider("Qauntidade de Restaurantes:", min_value=3, max_value=20, value=10)

#Quem desenvolveu a pagina.
st.sidebar.markdown('### Powered by Elio Matheus')

#lista de comidas
list_cuisines = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author',
       'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African',
       'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian',
       'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts',
       'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food',
       'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun',
       'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish',
       'Deli', 'British', 'California', 'Others', 'Eastern European',
       'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie',
       'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese',
       'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental',
       'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi',
       'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food',
       'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai',
       'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi',
       'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad',
       'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan',
       'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian',
       'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western',
       'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti',
       'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African',
       'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets',
       'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner',
       'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç']
cuisines_lt = st.sidebar.multiselect('Escolha os Tipos de Culinária',
                      list_cuisines,
                      default=['Home-made','BBQ','Japanese', 'Brazilian','Arabian','American','Italian'])
#--------------------------------------------------------------------------------
#Layout no Streamlit 
#--------------------------------------------------------------------------------
st.markdown( '# 🍽️ Visão Tipos de Cusinhas' )
st.markdown(' ## Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        label, value, ajuda = max_rating(df1,'Italian')
        col1.metric(label,value,help=ajuda)

    with col2:
        label, value, ajuda = max_rating(df1,'American')
        col2.metric(label,value,help=ajuda)
        
    with col3:
        label, value, ajuda = max_rating(df1,'Arabian')
        col3.metric(label,value,help=ajuda)
        
    with col4:       
        label, value, ajuda = max_rating(df1,'Japanese')
        col4.metric(label,value,help=ajuda)
        
    with col5:
        label, value, ajuda = max_rating(df1,'Brazilian')
        col5.metric(label,value,help=ajuda)

with st.container():
    st.markdown(f'## Top {barra} Restaurantes')
    dataframe = tops(df1)
    st.dataframe(dataframe.head(barra))
 


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = grafico_1(df1,barra)
        st.plotly_chart(fig,use_container_width=True,theme=None)
        
    with col2:
        fig = grafico_2(df1,barra)
        st.plotly_chart(fig,use_container_width=True,theme=None)









                            