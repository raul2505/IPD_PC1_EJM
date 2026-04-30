import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# =====================================
# CONFIG
# =====================================
st.set_page_config(page_title="ML Deportivo IPD", layout="wide")

st.title("🏅 Machine Learning - Rendimiento Deportivo")

# =====================================
# CARGA DE DATOS
# =====================================
archivo = r"C:\Users\erick\Desktop\IPD_PC1\Data_DeportistasEventos_0.xlsx"

@st.cache_data
def cargar_datos():
    return pd.read_excel(archivo)

df = cargar_datos()

# =====================================
# 1. DATA ORIGINAL
# =====================================
st.header("📁 Datos originales")
st.dataframe(df)

# =====================================
# 2. LIMPIEZA
# =====================================
st.header("🧹 Preparación de datos")

df = df.rename(columns={
    "FEDERACION": "DEPORTE",
    "EVENTO": "EVENTO",
    "DEPORTISTA": "NOMBRE",
    "PUESTO": "RESULTADO"
})

# Fecha → año
df["FECHA_INICIO"] = pd.to_datetime(df["FECHA_INICIO"], format="%Y%m%d", errors="coerce")
df["AÑO"] = df["FECHA_INICIO"].dt.year

# Limpiar texto
df["RESULTADO"] = (
    df["RESULTADO"]
    .astype(str)
    .str.upper()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Clasificar medalla
df["MEDALLA"] = df["RESULTADO"].apply(
    lambda x: 1 if x in ["ORO", "PLATA", "BRONCE"] else 0
)

# =====================================
# 3. FEATURES
# =====================================
st.header("🧠 Feature Engineering")

# Variables simples (puedes mejorar esto si quieres más nota)
df["ES_COLECTIVO"] = (df["COLECTIVO"] == "Colectivo").astype(int)

# Convertir categóricas
df_ml = pd.get_dummies(df[[
    "DEPORTE",
    "ESPECIALIDAD",
    "ES_COLECTIVO"
]], drop_first=True)

# Target
y = df["MEDALLA"]

# Rellenar nulos
X = df_ml.fillna(0)

st.write("Shape X:", X.shape)
st.write("Shape y:", y.shape)

# =====================================
# 4. SPLIT
# =====================================
st.header("✂️ División Train/Test")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================
# 5. MODELO
# =====================================
st.header("🤖 Entrenamiento")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

st.success("Modelo entrenado")

# =====================================
# 6. PREDICCIONES
# =====================================
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# =====================================
# 7. EVALUACIÓN
# =====================================
st.header("📊 Evaluación")

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

col1, col2 = st.columns(2)
col1.metric("Train Accuracy", f"{train_acc:.4f}")
col2.metric("Test Accuracy", f"{test_acc:.4f}")

# Matriz de confusión
st.subheader("Matriz de confusión")
cm = confusion_matrix(y_test, y_test_pred)
st.write(cm)

fig, ax = plt.subplots()
ax.imshow(cm)
ax.set_title("Matriz de Confusión")
st.pyplot(fig)

# Reporte
st.subheader("Reporte de clasificación")
st.text(classification_report(y_test, y_test_pred))

# =====================================
# 8. DIAGNÓSTICO
# =====================================
st.header("🧠 Diagnóstico")

if train_acc - test_acc > 0.1:
    st.warning("Posible OVERFITTING")
elif train_acc < 0.6 and test_acc < 0.6:
    st.error("Posible UNDERFITTING")
else:
    st.success("Modelo balanceado")

# =====================================
# 9. CLUSTERING
# =====================================
st.header("🔍 Clustering de participaciones")

# Variables numéricas simples
X_cluster = df[["AÑO"]].fillna(0)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X_cluster)

st.subheader("Resumen por cluster")
st.dataframe(df.groupby("cluster")[["AÑO"]].mean())

# =====================================
# 10. VISUALIZACIÓN CLUSTER
# =====================================
st.subheader("Visualización clustering")

fig2, ax2 = plt.subplots()
scatter = ax2.scatter(df["AÑO"], df["MEDALLA"], c=df["cluster"])
ax2.set_xlabel("AÑO")
ax2.set_ylabel("Medalla (1=Sí, 0=No)")
ax2.set_title("Clustering de Participaciones")

st.pyplot(fig2)

# =====================================
# 11. CONCLUSIÓN
# =====================================
st.header("📌 Conclusión")

st.info("""
Se aplicó un modelo de clasificación para predecir si un deportista obtiene medalla.

El modelo tiene capacidad predictiva limitada porque:
- Hay pocas variables relevantes
- No se incluyen factores como nivel del evento o competencia

El clustering permitió identificar patrones de participación,
aunque con variables simples.

Este análisis es exploratorio y puede mejorarse con más datos.
""")