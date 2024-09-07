#pip install stramlit

import streamlit as st
import pandas as pd
import sqlite3

# conectar no banco de dados SQLite
conn = sqlite3.connect('E:\projeto_scraping\src\data\quotes.db')

# carregar os dados da tabela 'mercadolivre_itens' 
df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)

#fechar conexao com banco
conn.close()

#titulo da aplciação
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

st.subheader('KPIs principais do sistema')
# criacao de uma tabela, em que cada variavel e uma coluna:
col1, col2, col3 = st.columns(3)


#Mostrar tabela com dados no dashboard:
#st.write(df)

#KP1 - Número total de itens
total_itens = df.shape[0]
col1.metric(label="Número Total de Itens", value=total_itens)

#KP2 - Número de marcas
unique_brands = df['brand'].nunique()
col2.metric(label="Número de Marcas Únicas", value=unique_brands)

#KP3 - Preço médio novo em reais
total_itens = df.shape[0]
average_new_prince = df['new_price'].mean()
col3.metric(label="Preço Médio Novo (R$)", value=f"{average_new_prince:.2f}")

# marcas mais encontrdas ate a pagina 10
st.subheader("Marcas mais encontradas até a 10ª página")
#col1 terá 4 partes proporcionais
#col2 terá 2 partes proporcionais
col1, col2 = st.columns([4,2])
#sort_values -> colocar em ordem alfabética
top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)


# preco medio por marca 
st.subheader("Preço médio por marca")
col1, col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)


#satisfação total por marca
st.subheader("Satisfação total por marca")
col1, col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)

