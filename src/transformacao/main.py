import pandas as pd
import sqlite3 
from datetime import datetime

# Setando o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Criando nosso df
df = pd.read_json("E:\projeto_scraping\src\data\data.jsonl", lines=True)

# Adicionando colunas 
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'

df['_data_coleta'] = datetime.now()


# JSON Considera tudo como String, vamos precisar ajustar os tipos dos dados
# Alterando os tipos de dados para float e limpando dados nulos 
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#removendo parenteses do review amount
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#tratar os precos como float e calcular valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# remover as colunas antigas de preco
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

#conectar no bd
# o banco de dados sqlite tem um arquitetura em que roda no cliente , nao precisa subir um servidor de bd (como postgres)
conn = sqlite3.connect('E:\projeto_scraping\src\data\quotes.db')

#salvar no bd
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)


#fechar conexao com bd
conn.close()

print(df.head())