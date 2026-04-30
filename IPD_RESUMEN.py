# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:43:58 2026

@author: erick
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Deportivo IPD", layout="wide")

st.title("🏅 Dashboard - Rendimiento Deportivo Internacional")
st.write("Análisis de participación y resultados de deportistas peruanos")

# -------------------------
# CARGA DE DATOS
# -------------------------
archivo = r"C:\Users\erick\Desktop\IPD_PC1\Data_DeportistasEventos_0.xlsx" # <-- CAMBIA ESTO

df = pd.read_excel(archivo, index_col = False)

# -------------------------
# LIMPIEZA DE DATOS
# -------------------------

# Renombrar columnas (opcional si quieres simplificar)
df = df.rename(columns={
    "FEDERACION": "DEPORTE",
    "EVENTO": "EVENTO_INTERNACIONAL",
    "DEPORTISTA": "NOMBRE",
    "PUESTO": "RESULTADO"
})

# Convertir fechas
df["FECHA_INICIO"] = pd.to_datetime(df["FECHA_INICIO"], format="%Y%m%d", errors="coerce")

# Crear columna AÑO
df["AÑO"] = df["FECHA_INICIO"].dt.year

# Limpiar texto
df["RESULTADO"] = df["RESULTADO"].astype(str).str.upper().str.strip()

# Crear columna MEDALLA correctamente
df["MEDALLA"] = df["RESULTADO"].apply(lambda x: x if x in ["ORO", "PLATA", "BRONCE"] else "SIN MEDALLA")

# Eliminar nulos importantes
df = df.dropna(subset=["NOMBRE", "DEPORTE", "EVENTO_INTERNACIONAL"])

# -------------------------
# MÉTRICAS GENERALES
# -------------------------
st.subheader("📌 Resumen general")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total registros", len(df))
col2.metric("Total deportistas", df["NOMBRE"].nunique())
col3.metric("Total eventos", df["EVENTO_INTERNACIONAL"].nunique())
col4.metric("Total deportes", df["DEPORTE"].nunique())

col5, col6, col7, col8 = st.columns(4)

col5.metric("🥇 Oro", (df["MEDALLA"] == "ORO").sum())
col6.metric("🥈 Plata", (df["MEDALLA"] == "PLATA").sum())
col7.metric("🥉 Bronce", (df["MEDALLA"] == "BRONCE").sum())
col8.metric("Sin medalla", (df["MEDALLA"] == "SIN MEDALLA").sum())

# -------------------------
# FILTROS
# -------------------------
st.sidebar.header("🔎 Filtros")

deporte = st.sidebar.selectbox("Deporte", ["Todos"] + sorted(df["DEPORTE"].unique()))
if deporte != "Todos":
    df = df[df["DEPORTE"] == deporte]

anio = st.sidebar.selectbox("Año", ["Todos"] + sorted(df["AÑO"].dropna().unique()))
if anio != "Todos":
    df = df[df["AÑO"] == anio]

# -------------------------
# TABLA
# -------------------------
st.subheader("📄 Datos")
st.dataframe(df, use_container_width=True)

# -------------------------
# GRÁFICO 1: MEDALLAS POR DEPORTE
# -------------------------
st.subheader("🏅 Medallas por deporte")

df_medallas = df[df["MEDALLA"] != "SIN MEDALLA"]

medallas_dep = df_medallas.groupby(["DEPORTE", "MEDALLA"]).size().reset_index(name="TOTAL")

fig1 = px.bar(
    medallas_dep,
    x="DEPORTE",
    y="TOTAL",
    color="MEDALLA",
    barmode="group",
    title="Medallas por disciplina"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# GRÁFICO 2: PARTICIPACIÓN POR EVENTO
# -------------------------
st.subheader("🌍 Participación por evento internacional")

eventos = df["EVENTO_INTERNACIONAL"].value_counts().reset_index()
eventos.columns = ["EVENTO", "PARTICIPACIONES"]

fig2 = px.bar(
    eventos,
    x="EVENTO",
    y="PARTICIPACIONES",
    title="Cantidad de participaciones por evento"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# GRÁFICO 3: EVOLUCIÓN HISTÓRICA
# -------------------------
st.subheader("📈 Evolución de resultados")

evolucion = df.groupby(["AÑO", "MEDALLA"]).size().reset_index(name="TOTAL")

fig3 = px.line(
    evolucion,
    x="AÑO",
    y="TOTAL",
    color="MEDALLA",
    markers=True,
    title="Evolución de resultados por año"
)

st.plotly_chart(fig3, use_container_width=True)