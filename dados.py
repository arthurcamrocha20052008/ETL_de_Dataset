import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. CARREGAMENTO DO ARQUIVO
# ============================================================

caminho_arquivo = r"C:\Users\camis\Downloads\Dataset_Hospital_ETL_50mil.xlsx"

df = pd.read_excel(
    caminho_arquivo,
    sheet_name="Atendimentos"
)

print("--- Primeiras linhas da base original ---")
print(df.head())


## ============================================================
# 2. TRATAMENTO E LIMPEZA DOS DADOS
# ============================================================

# ------------------------------------------------------------
# 1. Remove linhas inteiramente vazias
# ------------------------------------------------------------

df = df.dropna(how="all")


# ------------------------------------------------------------
# 2. Remove registros duplicados
# ------------------------------------------------------------

df = df.drop_duplicates()


# ------------------------------------------------------------
# 3. Limpeza dos espaços em todas as colunas de texto
# ------------------------------------------------------------

colunas_texto = df.select_dtypes(
    include=["object", "string"]
).columns

for coluna in colunas_texto:
    df[coluna] = (
        df[coluna]
        .astype("string")
        .str.strip()
    )


# ------------------------------------------------------------
# 4. Padronização das cidades
# ------------------------------------------------------------

df["cidade"] = (
    df["cidade"]
    .astype("string")
    .str.strip()
    .str.title()
)


# ------------------------------------------------------------
# 5. Padronização dos convênios
# ------------------------------------------------------------

df["convenio"] = (
    df["convenio"]
    .astype("string")
    .str.strip()
    .str.upper()
)


# ------------------------------------------------------------
# 6. Padronização de hospital
# ------------------------------------------------------------

df["hospital"] = (
    df["hospital"]
    .astype("string")
    .str.strip()
    .str.title()
)


# ------------------------------------------------------------
# 7. Padronização de especialidade
# ------------------------------------------------------------

df["especialidade"] = (
    df["especialidade"]
    .astype("string")
    .str.strip()
    .str.title()
)


# ------------------------------------------------------------
# 8. Tratamento do valor de atendimento
# ------------------------------------------------------------

df["valor_atendimento"] = (
    df["valor_atendimento"]
    .astype("string")
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df["valor_atendimento"] = pd.to_numeric(
    df["valor_atendimento"],
    errors="coerce"
)


# ------------------------------------------------------------
# 9. Tratamento de valores negativos
# ------------------------------------------------------------

# Quantidade negativa vira zero
df.loc[
    df["quantidade"] < 0,
    "quantidade"
] = 0

# Valor de atendimento negativo vira zero
df.loc[
    df["valor_atendimento"] < 0,
    "valor_atendimento"
] = 0


# ------------------------------------------------------------
# 10. Conversão da quantidade para número
# ------------------------------------------------------------

df["quantidade"] = pd.to_numeric(
    df["quantidade"],
    errors="coerce"
)


# ------------------------------------------------------------
# 11. Conversão das datas
# ------------------------------------------------------------

df["data_atendimento"] = pd.to_datetime(
    df["data_atendimento"],
    errors="coerce",
    dayfirst=True
)


# ------------------------------------------------------------
# 12. Remoção de registros sem data
# ------------------------------------------------------------

df = df.dropna(
    subset=["data_atendimento"]
)


# ------------------------------------------------------------
# 13. Preenchimento de valores ausentes
# ------------------------------------------------------------

df["quantidade"] = df["quantidade"].fillna(0)

df["valor_atendimento"] = (
    df["valor_atendimento"]
    .fillna(0)
)

df["convenio"] = (
    df["convenio"]
    .fillna("NAO INFORMADO")
)

df["cidade"] = (
    df["cidade"]
    .fillna("NAO INFORMADA")
)

df["hospital"] = (
    df["hospital"]
    .fillna("NAO INFORMADO")
)

df["especialidade"] = (
    df["especialidade"]
    .fillna("NAO INFORMADA")
)


# ------------------------------------------------------------
# 14. Criação de novas informações a partir da data
# ------------------------------------------------------------

df["ano"] = (
    df["data_atendimento"].dt.year
)

df["mes"] = (
    df["data_atendimento"].dt.month
)

df["dia_semana"] = (
    df["data_atendimento"].dt.day_name()
)


# ------------------------------------------------------------
# 15. Criação de faixa de valor do atendimento
# ------------------------------------------------------------

df["faixa_valor"] = pd.cut(
    df["valor_atendimento"],
    bins=[
        0,
        100,
        300,
        500,
        float("inf")
    ],
    labels=[
        "Até R$ 100",
        "R$ 101 - R$ 300",
        "R$ 301 - R$ 500",
        "Acima de R$ 500"
    ]
)


# ------------------------------------------------------------
# 16. Identificação de valores muito altos ou muito baixos
#    usando IQR
# ------------------------------------------------------------

Q1 = df["valor_atendimento"].quantile(0.25)
Q3 = df["valor_atendimento"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

df["outlier_valor"] = (
    (df["valor_atendimento"] < limite_inferior) |
    (df["valor_atendimento"] > limite_superior)
)


# ------------------------------------------------------------
# 17. Verificação de valores únicos
# ------------------------------------------------------------

print("\n--- Valores únicos ---")

print("\nHospitais:")
print(df["hospital"].unique())

print("\nConvênios:")
print(df["convenio"].unique())

print("\nEspecialidades:")
print(df["especialidade"].unique())

print("\nCidades:")
print(df["cidade"].unique())


# ------------------------------------------------------------
# 18. Verificação de valores ausentes
# ------------------------------------------------------------

print("\n--- Valores ausentes ---")

print(
    df.isnull().sum()
)


# ------------------------------------------------------------
# 19. Verificação de duplicados
# ------------------------------------------------------------

print("\n--- Duplicados ---")

print(
    "Duplicados restantes:",
    df.duplicated().sum()
)


# ============================================================
# 3. INFORMAÇÕES DA BASE TRATADA
# ============================================================

print("\n============================================================")
print("INFORMAÇÕES DA BASE TRATADA")
print("============================================================")

print(
    "\nQuantidade de registros:",
    len(df)
)

print(
    "\nQuantidade de colunas:",
    len(df.columns)
)

print("\nColunas disponíveis:")

print(
    df.columns.tolist()
)


# ------------------------------------------------------------
# Informações sobre as datas
# ------------------------------------------------------------

print(
    "\nDatas inválidas:",
    df["data_atendimento"].isna().sum()
)

print(
    "Data mais antiga:",
    df["data_atendimento"].min()
)

print(
    "Data mais recente:",
    df["data_atendimento"].max()
)


# ------------------------------------------------------------
# Informações sobre valores
# ------------------------------------------------------------

print(
    "\nValor mínimo:",
    df["valor_atendimento"].min()
)

print(
    "Valor máximo:",
    df["valor_atendimento"].max()
)

print(
    "Valor médio:",
    df["valor_atendimento"].mean()
)


# ------------------------------------------------------------
# Informações sobre quantidade
# ------------------------------------------------------------

print(
    "\nQuantidade mínima:",
    df["quantidade"].min()
)

print(
    "Quantidade máxima:",
    df["quantidade"].max()
)

print(
    "Quantidade média:",
    df["quantidade"].mean()
)


# ------------------------------------------------------------
# Informações sobre outliers
# ------------------------------------------------------------

print(
    "\nQuantidade de possíveis outliers:",
    df["outlier_valor"].sum()
)


# ------------------------------------------------------------
# Primeiras linhas da base tratada
# ------------------------------------------------------------

print("\n--- Primeiras linhas da base tratada ---")

print(
    df.head()
)


# ============================================================
# 4. VISUALIZAÇÕES DE DADOS
# ============================================================

# ------------------------------------------------------------
# Gráfico 1: Atendimentos por Tipo
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

df["tipo_atendimento"].value_counts().plot(
    kind="bar"
)

plt.title("Quantidade de Consultas por Tipo")
plt.xlabel("Tipos de Consultas")
plt.ylabel("Quantidade de Consultas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Gráfico 2: Atendimentos por Especialidade
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

df["especialidade"].value_counts().plot(
    kind="bar"
)

plt.title("Quantidade de Atendimentos por Especialidade")
plt.xlabel("Especialidades")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Gráfico 3: Atendimentos por Cidade
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

df["cidade"].value_counts().plot(
    kind="bar"
)

plt.title("Quantidade de Atendimentos por Cidade")
plt.xlabel("Cidades")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Gráfico 4: Distribuição por Convênio
# ------------------------------------------------------------

plt.figure(figsize=(6, 6))

df["convenio"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribuição de Atendimentos por Convênio")
plt.ylabel("")
plt.tight_layout()
plt.show()


# ============================================================
# 5. DESAFIOS
# ============================================================

# ------------------------------------------------------------
# Desafio 1: Proporção de Atendimentos por Hospital
# ------------------------------------------------------------

atendimento_hospital = df["hospital"].value_counts()

plt.figure(figsize=(6, 6))

atendimento_hospital.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Proporção de Atendimentos por Hospital")
plt.ylabel("")
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Desafio 2: Quantidade de Atendimentos por Hospital
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

atendimento_hospital.plot(
    kind="bar"
)

plt.title("Quantidade de Atendimentos por Hospital")
plt.xlabel("Hospitais")
plt.ylabel("Quantidade de Atendimentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()