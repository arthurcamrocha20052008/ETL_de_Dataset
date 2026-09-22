import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Carregamento do arquivo
caminho_arquivo = r'C:\Users\nicolas.lettieri\Downloads\BDI1\Dataset_Revisao_Hospital_50mil.xlsx'
df = pd.read_excel(caminho_arquivo, sheet_name="Atendimentos")

print("--- Primeiras linhas da base original ---")
print(df.head())

# 2. Tratamento e Limpeza dos Dados
# Remove linhas inteiramente vazias
df = df.dropna(how="all")

# Tratamento e conversão do valor de atendimento para float
df["valor_atendimento"] = (
    df["valor_atendimento"]
    .astype("string")
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
df["valor_atendimento"] = pd.to_numeric(df["valor_atendimento"], errors="coerce")

# Conversão de datas
df["data_atendimento"] = pd.to_datetime(df["data_atendimento"], errors="coerce", dayfirst=True)

# Correção de quantidades negativas
df.loc[df["quantidade"] < 0, "quantidade"] = 0

# Padronização da coluna de cidade (remove espaços e aplica Capitalização)
df["cidade"] = df["cidade"].astype("string").str.strip().str.title()

# Remoção de registros duplicados
df = df.drop_duplicates()

print("\n--- Informações da base tratada ---")
print("Colunas disponíveis:", df.columns.tolist())
print("Datas inválidas:", df["data_atendimento"].isna().sum())
print("Duplicados restantes:", df.duplicated().sum())
print(df.head())

# 3. Visualizações de Dados

# Gráfico 1: Atendimentos por Tipo
plt.figure(figsize=(8, 5))
df["tipo_atendimento"].value_counts().plot(kind="bar")
plt.title("Quantidade de Consultas por Tipo")
plt.xlabel("Tipos de Consultas")
plt.ylabel("Quantidade de Consultas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: Atendimentos por Especialidade
plt.figure(figsize=(10, 5))
df["especialidade"].value_counts().plot(kind="bar")
plt.title("Quantidade de Atendimentos por Especialidade")
plt.xlabel("Especialidades")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 3: Atendimentos por Cidade
plt.figure(figsize=(10, 5))
df["cidade"].value_counts().plot(kind="bar")
plt.title("Quantidade de Atendimentos por Cidade")
plt.xlabel("Cidades")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 4: Distribuição por Convênio (Pizza)
plt.figure(figsize=(6, 6))
df["convenio"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Distribuição de Atendimentos por Convênio")
plt.ylabel("")
plt.tight_layout()
plt.show()

# Gráfico DESAFIO 1: Proporção de Atendimentos por Hospital (Pizza)
plt.figure(figsize=(6, 6))
atendimento_hospital = df["hospital"].value_counts()
atendimento_hospital.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Proporção de Atendimentos por Hospital")
plt.ylabel("")
plt.tight_layout()
plt.show()

# Gráfico DESAFIO 2: Quantidade de Atendimentos por Hospital (Barras)
plt.figure(figsize=(8, 5))
atendimento_hospital.plot(kind="bar")
plt.title("Quantidade de Atendimentos por Hospital")
plt.xlabel("Hospitais")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)