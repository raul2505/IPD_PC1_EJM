# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:40:50 2026

@author: erick
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================================
# CONFIG DE PÁGINA
# =====================================
st.set_page_config(
    page_title="IPD – Análisis Deportivo",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# ESTILOS PERSONALIZADOS
# =====================================
st.markdown("""
<style>
    /* Fuente institucional */
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Barlow', sans-serif;
    }

    /* Fondo general */
    .stApp {
        background-color: #f4f6f9;
    }

    /* Header institucional */
    .ipd-header {
        background: linear-gradient(135deg, #c8102e 0%, #8b0000 60%, #1a1a2e 100%);
        padding: 2rem 2.5rem 1.5rem 2.5rem;
        border-radius: 0 0 16px 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(200,16,46,0.25);
    }
    .ipd-header h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 1px;
    }
    .ipd-header p {
        color: rgba(255,255,255,0.82);
        font-size: 1rem;
        margin: 0.3rem 0 0 0;
        font-weight: 400;
    }
    .ipd-flag {
        font-size: 2.8rem;
        margin-right: 12px;
        vertical-align: middle;
    }

    /* Tarjetas de métricas */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #c8102e;
        margin-bottom: 1rem;
    }
    .metric-title {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #aaa;
        margin-top: 2px;
    }

    /* Sección de pasos (user flow) */
    .step-badge {
        display: inline-block;
        background: #c8102e;
        color: white;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        padding: 2px 10px;
        border-radius: 20px;
        margin-bottom: 0.4rem;
        text-transform: uppercase;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1a1a2e;
    }
    section[data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
    }

    /* Interpretación */
    .interp-box {
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 0.5rem;
        font-size: 0.95rem;
        font-weight: 500;
    }
    .interp-alto {
        background: #e6f9f0;
        border-left: 5px solid #27ae60;
        color: #1a6b3a;
    }
    .interp-medio {
        background: #fff9e6;
        border-left: 5px solid #f1c40f;
        color: #7d6608;
    }
    .interp-bajo {
        background: #fdecea;
        border-left: 5px solid #e74c3c;
        color: #922b21;
    }

    /* Separador */
    hr.ipd-sep {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 1.5rem 0;
    }

    /* Sección títulos */
    .section-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        letter-spacing: 0.5px;
        margin-bottom: 0.2rem;
    }
    .section-sub {
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER INSTITUCIONAL
# =====================================
st.markdown("""
<div class="ipd-header">
    <div>
        <span class="ipd-flag">🇵🇪</span>
        <span style="font-family:'Barlow Condensed',sans-serif; font-size:2.4rem; font-weight:700; color:#fff; vertical-align:middle; letter-spacing:1px;">
            Instituto Peruano del Deporte
        </span>
    </div>
    <p style="margin-left:3.6rem;">Sistema de Análisis de Rendimiento Deportivo — Panel de Control</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# CARGA DE DATOS
# =====================================
ARCHIVO = r"C:\Users\erick\Desktop\IPD_PC1\Data_DeportistasEventos_0.xlsx"

@st.cache_data(show_spinner="Cargando datos del IPD...")
def cargar_datos():
    return pd.read_excel(ARCHIVO)

try:
    df_raw = cargar_datos()
except Exception as e:
    st.error(f"No se pudo cargar el archivo: {e}")
    st.stop()

# =====================================
# LIMPIEZA Y TRANSFORMACIÓN
# =====================================
df = df_raw.copy()

df = df.rename(columns={
    "FEDERACION": "DEPORTE",
    "EVENTO": "EVENTO",
    "DEPORTISTA": "ATLETA",
    "PUESTO": "RESULTADO"
})

df["FECHA_INICIO"] = pd.to_datetime(df["FECHA_INICIO"], format="%Y%m%d", errors="coerce")
df["AÑO"] = df["FECHA_INICIO"].dt.year
df["MES"] = df["FECHA_INICIO"].dt.month_name()

df["RESULTADO"] = df["RESULTADO"].astype(str).str.upper().str.strip()

MEDALLAS_VALIDAS = ["ORO", "PLATA", "BRONCE"]
df["MEDALLA"] = df["RESULTADO"].apply(
    lambda x: x if x in MEDALLAS_VALIDAS else "SIN MEDALLA"
)

COLOR_MEDALLAS = {
    "ORO":        "#FFD700",
    "PLATA":      "#B0BEC5",
    "BRONCE":     "#CD7F32",
    "SIN MEDALLA":"#E0E0E0",
}

# =====================================
# SIDEBAR — USER FLOW
# =====================================
with st.sidebar:
    st.markdown("## 🔍 Análisis Deportivo")
    st.markdown("**Paso 1 — Tipo de análisis**")
    tipo_filtro = st.radio(
        "Selecciona el enfoque:",
        ["Por Deporte", "Por Atleta", "Por Evento"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Paso 2 — Selección**")

    if tipo_filtro == "Por Deporte":
        opcion = st.selectbox("Deporte", sorted(df["DEPORTE"].dropna().unique()))
        df_filtrado = df[df["DEPORTE"] == opcion]
        titulo_filtro = f"Deporte: {opcion}"

    elif tipo_filtro == "Por Atleta":
        opcion = st.selectbox("Atleta", sorted(df["ATLETA"].dropna().unique()))
        df_filtrado = df[df["ATLETA"] == opcion]
        titulo_filtro = f"Atleta: {opcion}"

    else:
        opcion = st.selectbox("Evento", sorted(df["EVENTO"].dropna().unique()))
        df_filtrado = df[df["EVENTO"] == opcion]
        titulo_filtro = f"Evento: {opcion}"

    st.markdown("---")

    # Filtro adicional de años
    años_disponibles = sorted(df_filtrado["AÑO"].dropna().unique().astype(int))
    if len(años_disponibles) > 1:
        st.markdown("**Paso 3 — Rango de años (opcional)**")
        año_min, año_max = st.select_slider(
            "Rango",
            options=años_disponibles,
            value=(años_disponibles[0], años_disponibles[-1]),
            label_visibility="collapsed"
        )
        df_filtrado = df_filtrado[
            df_filtrado["AÑO"].between(año_min, año_max)
        ]

    st.markdown("---")
    st.caption("Instituto Peruano del Deporte · IPD")

# =====================================
# PASO 3: MÉTRICAS PRINCIPALES
# =====================================
st.markdown(f'<div class="step-badge">Paso 3 — Resultados para {titulo_filtro}</div>', unsafe_allow_html=True)

total        = len(df_filtrado)
total_oro    = (df_filtrado["MEDALLA"] == "ORO").sum()
total_plata  = (df_filtrado["MEDALLA"] == "PLATA").sum()
total_bronce = (df_filtrado["MEDALLA"] == "BRONCE").sum()
total_med    = total_oro + total_plata + total_bronce
pct_med      = (total_med / total * 100) if total > 0 else 0
eventos_u    = df_filtrado["EVENTO"].nunique()
atletas_u    = df_filtrado["ATLETA"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Participaciones</div>
        <div class="metric-value">{total:,}</div>
        <div class="metric-sub">registros totales</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-color:#FFD700;">
        <div class="metric-title">🥇 Oro</div>
        <div class="metric-value" style="color:#b8860b;">{total_oro}</div>
        <div class="metric-sub">medallas de oro</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-color:#B0BEC5;">
        <div class="metric-title">🥈 Plata</div>
        <div class="metric-value" style="color:#607d8b;">{total_plata}</div>
        <div class="metric-sub">medallas de plata</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-color:#CD7F32;">
        <div class="metric-title">🥉 Bronce</div>
        <div class="metric-value" style="color:#8d5524;">{total_bronce}</div>
        <div class="metric-sub">medallas de bronce</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="border-color:#1a1a2e;">
        <div class="metric-title">Tasa de medallas</div>
        <div class="metric-value" style="color:#1a1a2e;">{pct_med:.1f}%</div>
        <div class="metric-sub">{eventos_u} eventos · {atletas_u} atletas</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="ipd-sep">', unsafe_allow_html=True)

# =====================================
# PASO 4: VISUALIZACIÓN DE DESEMPEÑO
# =====================================
st.markdown('<div class="step-badge">Paso 4 — Visualización de desempeño</div>', unsafe_allow_html=True)
st.markdown("")

# --- Fila 1: Medallas + Evolución temporal ---
col_a, col_b = st.columns([1, 2])

with col_a:
    st.markdown('<div class="section-title">🏅 Distribución de resultados</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Proporción de medallas obtenidas</div>', unsafe_allow_html=True)

    medallas_cnt = df_filtrado["MEDALLA"].value_counts().reset_index()
    medallas_cnt.columns = ["MEDALLA", "CANTIDAD"]

    orden = ["ORO", "PLATA", "BRONCE", "SIN MEDALLA"]
    medallas_cnt["MEDALLA"] = pd.Categorical(medallas_cnt["MEDALLA"], categories=orden, ordered=True)
    medallas_cnt = medallas_cnt.sort_values("MEDALLA")

    fig_pie = px.pie(
        medallas_cnt,
        names="MEDALLA",
        values="CANTIDAD",
        color="MEDALLA",
        color_discrete_map=COLOR_MEDALLAS,
        hole=0.45,
    )
    fig_pie.update_traces(
        textposition="outside",
        textinfo="percent+label",
        pull=[0.04, 0.04, 0.04, 0],
    )
    fig_pie.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    st.markdown('<div class="section-title">📈 Evolución temporal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Participaciones y medallas por año</div>', unsafe_allow_html=True)

    evolucion = df_filtrado.groupby("AÑO").agg(
        TOTAL=("MEDALLA", "count"),
        MEDALLAS=("MEDALLA", lambda x: (x != "SIN MEDALLA").sum())
    ).reset_index()

    fig_evo = go.Figure()
    fig_evo.add_trace(go.Bar(
        x=evolucion["AÑO"], y=evolucion["TOTAL"],
        name="Participaciones", marker_color="#d0d8e8",
    ))
    fig_evo.add_trace(go.Scatter(
        x=evolucion["AÑO"], y=evolucion["MEDALLAS"],
        name="Medallas", mode="lines+markers",
        line=dict(color="#c8102e", width=2.5),
        marker=dict(size=7, color="#c8102e"),
    ))
    fig_evo.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#eee"),
        height=300,
    )
    st.plotly_chart(fig_evo, use_container_width=True)

st.markdown("")

# --- Fila 2: Participación por evento + ranking atletas ---
col_c, col_d = st.columns([3, 2])

with col_c:
    st.markdown('<div class="section-title">🌍 Participación por evento</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Cantidad de registros según el evento internacional</div>', unsafe_allow_html=True)

    eventos_df = (
        df_filtrado.groupby("EVENTO")
        .agg(
            TOTAL=("MEDALLA", "count"),
            MEDALLAS=("MEDALLA", lambda x: (x != "SIN MEDALLA").sum())
        )
        .reset_index()
        .sort_values("TOTAL", ascending=True)
        .tail(15)
    )

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=eventos_df["EVENTO"], x=eventos_df["TOTAL"],
        orientation="h", name="Participaciones",
        marker_color="#c8102e", opacity=0.85,
    ))
    fig_bar.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#eee"),
        yaxis=dict(showgrid=False),
        showlegend=False,
        height=max(250, len(eventos_df) * 28),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_d:
    if tipo_filtro != "Por Atleta":
        st.markdown('<div class="section-title">🏆 Top atletas</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Por total de medallas obtenidas</div>', unsafe_allow_html=True)

        top_atletas = (
            df_filtrado[df_filtrado["MEDALLA"] != "SIN MEDALLA"]
            .groupby("ATLETA")["MEDALLA"]
            .count()
            .reset_index()
            .rename(columns={"MEDALLA": "MEDALLAS"})
            .sort_values("MEDALLAS", ascending=False)
            .head(10)
        )

        if not top_atletas.empty:
            fig_top = px.bar(
                top_atletas,
                x="MEDALLAS", y="ATLETA",
                orientation="h",
                color="MEDALLAS",
                color_continuous_scale=["#f9d0d7", "#c8102e"],
            )
            fig_top.update_layout(
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#eee"),
                yaxis=dict(showgrid=False, autorange="reversed"),
                height=max(250, len(top_atletas) * 32),
            )
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("No hay medallas registradas para mostrar ranking.")
    else:
        st.markdown('<div class="section-title">🎯 Desglose por tipo de medalla</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Historial del atleta seleccionado</div>', unsafe_allow_html=True)

        desglose = df_filtrado["MEDALLA"].value_counts().reset_index()
        desglose.columns = ["MEDALLA", "TOTAL"]
        desglose["COLOR"] = desglose["MEDALLA"].map(COLOR_MEDALLAS)

        fig_dsg = px.bar(
            desglose, x="MEDALLA", y="TOTAL",
            color="MEDALLA",
            color_discrete_map=COLOR_MEDALLAS,
        )
        fig_dsg.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#eee"),
            height=280,
        )
        st.plotly_chart(fig_dsg, use_container_width=True)

st.markdown('<hr class="ipd-sep">', unsafe_allow_html=True)

# =====================================
# PASO 5: DETALLE DE DATOS
# =====================================
st.markdown('<div class="step-badge">Paso 5 — Detalle de registros</div>', unsafe_allow_html=True)
st.markdown("")

col_tbl, col_dl = st.columns([4, 1])
with col_tbl:
    st.markdown('<div class="section-title">📄 Tabla de datos filtrados</div>', unsafe_allow_html=True)

cols_mostrar = [c for c in ["ATLETA", "DEPORTE", "EVENTO", "FECHA_INICIO", "AÑO", "RESULTADO", "MEDALLA"] if c in df_filtrado.columns]

st.dataframe(
    df_filtrado[cols_mostrar].reset_index(drop=True),
    use_container_width=True,
    height=250,
)

with col_dl:
    st.markdown("")
    st.markdown("")
    csv = df_filtrado[cols_mostrar].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar CSV",
        data=csv,
        file_name=f"IPD_{opcion.replace(' ', '_')}.csv",
        mime="text/csv",
    )

st.markdown('<hr class="ipd-sep">', unsafe_allow_html=True)

# =====================================
# PASO 6: INTERPRETACIÓN AUTOMÁTICA
# =====================================
st.markdown('<div class="step-badge">Paso 6 — Interpretación de resultados</div>', unsafe_allow_html=True)
st.markdown("")

st.markdown('<div class="section-title">🧠 Diagnóstico de rendimiento</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Análisis automático basado en los datos filtrados</div>', unsafe_allow_html=True)
st.markdown("")

if total > 0:
    col_i1, col_i2 = st.columns(2)

    # --- Rendimiento general ---
    with col_i1:
        if pct_med > 50:
            nivel, clase, icono = "Alto rendimiento", "interp-alto", "✅"
            texto = (
                f"El {pct_med:.1f}% de las participaciones terminaron en medalla, "
                f"lo que indica un rendimiento superior al promedio esperado. "
                f"Se obtuvieron {total_med} medallas en {total} participaciones."
            )
        elif pct_med > 20:
            nivel, clase, icono = "Rendimiento moderado", "interp-medio", "⚠️"
            texto = (
                f"El {pct_med:.1f}% de participaciones terminaron en medalla. "
                f"Hay oportunidades claras de mejora para aumentar la tasa de éxito. "
                f"Se obtuvieron {total_med} medallas en {total} participaciones."
            )
        else:
            nivel, clase, icono = "Rendimiento bajo", "interp-bajo", "❌"
            texto = (
                f"Solo el {pct_med:.1f}% de participaciones terminaron en medalla. "
                f"Se recomienda revisar los procesos de preparación y selección de eventos. "
                f"Se obtuvieron {total_med} medallas en {total} participaciones."
            )

        st.markdown(f"""
        <div class="interp-box {clase}">
            <strong>{icono} {nivel}</strong><br><br>
            {texto}
        </div>""", unsafe_allow_html=True)

    # --- Análisis de tendencia ---
    with col_i2:
        if len(evolucion) >= 2:
            ult_2 = evolucion.tail(2)
            delta = int(ult_2.iloc[-1]["MEDALLAS"]) - int(ult_2.iloc[-2]["MEDALLAS"])
            año_ult = int(ult_2.iloc[-1]["AÑO"])
            if delta > 0:
                tend_clase, tend_icono, tend_txt = "interp-alto", "📈", f"Las medallas aumentaron en {delta} respecto al año anterior."
            elif delta < 0:
                tend_clase, tend_icono, tend_txt = "interp-bajo", "📉", f"Las medallas disminuyeron en {abs(delta)} respecto al año anterior."
            else:
                tend_clase, tend_icono, tend_txt = "interp-medio", "➡️", "El número de medallas se mantuvo estable respecto al año anterior."

            st.markdown(f"""
            <div class="interp-box {tend_clase}">
                <strong>{tend_icono} Tendencia reciente ({año_ult})</strong><br><br>
                {tend_txt} En {año_ult} se obtuvieron {int(ult_2.iloc[-1]['MEDALLAS'])} medallas de {int(ult_2.iloc[-1]['TOTAL'])} participaciones.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="interp-box interp-medio">
                <strong>➡️ Datos insuficientes para tendencia</strong><br><br>
                Se requieren datos de al menos 2 años para calcular la tendencia.
            </div>""", unsafe_allow_html=True)
else:
    st.warning("No hay datos disponibles para la selección actual.")

# =====================================
# FOOTER
# =====================================
st.markdown("")
st.markdown("---")
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    st.caption("🇵🇪 Instituto Peruano del Deporte (IPD) — Sistema de Análisis de Rendimiento Deportivo")
with col_f2:
    st.caption("Desarrollado con Streamlit · Python")