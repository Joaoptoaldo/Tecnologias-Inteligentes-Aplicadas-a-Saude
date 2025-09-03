import pandas as pd 

# === 1. Ler o CSV e limpar colunas vazias ===
df = pd.read_csv("glicose_data.csv")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  # remove colunas extras sem nome

print(" Colunas carregadas:", df.columns.tolist())
print(" Exemplo de linha:\n", df.iloc[0].to_dict())

# === 2. Mapeamentos para transformar categorias em números ===
map_glicemia = {"Baixo": 0, "Normal": 1, "Acima": 2}
map_kcal = {"Abaixo": 0, "Recomendado": 1, "Acima": 2}
map_carb = {"Abaixo": 0, "Normal": 1, "Acima": 2}

# Criar cópia do dataframe apenas com valores numéricos
df_num = df.copy()

df_num["GLICEMIA"] = df["GLICEMIA"].map(map_glicemia)
df_num["KCAL"] = df["KCAL"].map(map_kcal)
df_num["CARB"] = df["CARB"].map(map_carb)

# Converter demais colunas numéricas (se tiver texto vira NaN → depois tratamos)
for col in ["INSULINA", "SONO", "padel", "musculacao_R", "musculacao_H",
            "pilates", "corrida", "caminhada", "tenis", "sauna",
            "bike", "natacao", "eliptico", "volei_areia"]:
    df_num[col] = pd.to_numeric(df[col], errors="coerce")

# === 3. Estatísticas básicas ===
def resumo(col):
    serie = df_num[col].dropna()
    return {
        "Qtd valores válidos": len(serie),
        "Média": round(serie.mean(), 2) if not serie.empty else None,
        "Mediana": round(serie.median(), 2) if not serie.empty else None,
        "Mínimo": serie.min() if not serie.empty else None,
        "Máximo": serie.max() if not serie.empty else None
    }

print("\n Resumo estatístico:")
for coluna in ["GLICEMIA", "KCAL", "CARB", "INSULINA", "SONO"]:
    print(f"\n{coluna}:")
    for k, v in resumo(coluna).items():
        print(f"  {k}: {v}")