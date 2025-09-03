# PROJETO: Predição de glicemia com machine learning
# usando pandas, numpy, scikit-learn e matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns

# carrega os dados
df = pd.read_csv("glicose_data.csv")

print("Colunas do arquivo:", df.columns.tolist())
print("\nExemplo de dados:\n", df.head())

# mapeia variáveis categóricas para números
mapa_glicemia = {"Baixo": 0, "Normal": 1, "Acima": 2}   # <-- corrigido
mapa_kcal = {"Abaixo": 0, "Recomendado": 1, "Acima": 2} # <-- adicionado "Recomendado"
mapa_carb = {"Abaixo": 0, "Normal": 1, "Acima": 2}

df["GLICEMIA"] = df["GLICEMIA"].map(mapa_glicemia)
df["KCAL"] = df["KCAL"].map(mapa_kcal)
df["CARB"] = df["CARB"].map(mapa_carb)

# remove colunas desnecessárias Unnamed 
df = df.drop(columns=["Unnamed: 20", "Unnamed: 21"], errors="ignore")

# remove linhas com valores ausentes em colunas
df = df.dropna(subset=["GLICEMIA", "SONO", "KCAL", "CARB", "padel"])

print("\nTamanho final da base após limpeza:", df.shape)

# seleção das variáveis (X = entradas, y = alvo)
X = df[["SONO", "KCAL", "CARB", "padel"]]
y = df["GLICEMIA"]

# separa treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# treina modelo 
# Decision Tree
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

# predições
y_pred = modelo.predict(X_test)

# avaliação do modelo
print("\nAcurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))

# matriz de confusão
plt.figure(figsize=(6,5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues",
            xticklabels=["Baixo","Normal","Acima"], yticklabels=["Baixo","Normal","Acima"])
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.title("Matriz de Confusão - Predição de Glicemia")
plt.show()

# importância das variáveis
importancias = modelo.feature_importances_
plt.figure(figsize=(6,4))
plt.bar(X.columns, importancias, color="skyblue")
plt.title("Importância das Variáveis")
plt.ylabel("Peso no Modelo")
plt.show()
