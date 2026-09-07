import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Supply Chain & Fleet Control", layout="wide", page_icon="🚚")

# ==============================================================================
# SIMULADOR DE GEMELO DIGITAL LOGÍSTICO (DATA SINTÉTICA)
# ==============================================================================
@st.cache_data
def generar_flota():
    np.random.seed(101)
    n_rutas = 300
    # Centro de Distribución: Distrito Nacional (tierra firme)
    lat_base, lon_base = 18.4800, -69.9300 
    
    data = pd.DataFrame({
        "ID_Ruta": [f"RT-{i:04d}" for i in range(1, n_rutas+1)],
        "Vehiculo": np.random.choice(["Camión Frigorífico", "Furgón Ligero", "Moto Delivery"], n_rutas, p=[0.2, 0.5, 0.3]),
        "Conductor": np.random.choice(["Juan P.", "Miguel R.", "Luis S.", "Ana M.", "Carlos T."], n_rutas),
        "lat": np.random.normal(lat_base, 0.02, n_rutas), # Reducida la desviación para no caer al mar
        "lon": np.random.normal(lon_base, 0.02, n_rutas),
        "Estatus": np.random.choice(["Entregado", "En Ruta", "Demorado", "Alerta Mecánica"], n_rutas, p=[0.60, 0.25, 0.10, 0.05]),
        "Satisfaccion_Cliente": np.random.randint(1, 6, n_rutas),
        "Valor_Carga_USD": np.random.uniform(500, 15000, n_rutas)
    })
    
    # Asignar colores Hex según estatus para el Mapa de Streamlit
    color_map = {
        "Entregado": "#22c55e",      # Verde
        "En Ruta": "#3b82f6",        # Azul
        "Demorado": "#f59e0b",       # Amarillo
        "Alerta Mecánica": "#ef4444" # Rojo
    }
    data["Color"] = data["Estatus"].map(color_map)
    data["Size"] = data["Valor_Carga_USD"] / 100  # Puntos más grandes = más dinero
    return data

df_geo = generar_flota()

# ==============================================================================
# BARRA LATERAL (CONTROL TOWER)
# ==============================================================================
st.sidebar.title("📡 Torre de Control")
filtro_estatus = st.sidebar.multiselect(
    "Filtrar por Estatus Operativo:", 
    options=df_geo["Estatus"].unique(),
    default=["En Ruta", "Demorado", "Alerta Mecánica"]
)

filtro_vehiculo = st.sidebar.selectbox("Tipo de Flota:", ["Toda la Flota"] + list(df_geo["Vehiculo"].unique()))

# Aplicar Filtros
df_filtrado = df_geo[df_geo["Estatus"].isin(filtro_estatus)]
if filtro_vehiculo != "Toda la Flota":
    df_filtrado = df_filtrado[df_filtrado["Vehiculo"] == filtro_vehiculo]

# ==============================================================================
# PANEL PRINCIPAL
# ==============================================================================
st.title("🚚 Centro de Operaciones y GeoTracking")
st.markdown("Monitoreo en tiempo real de la cadena de suministro, estatus de entregas y riesgo financiero en tránsito.")

# KPIs Ejecutivos
c1, c2, c3, c4 = st.columns(4)
c1.metric("Unidades en Pantalla", len(df_filtrado))
c2.metric("Valor en Tránsito (Riesgo)", f"${df_filtrado[df_filtrado['Estatus'] != 'Entregado']['Valor_Carga_USD'].sum():,.0f}")
alertas = len(df_filtrado[df_filtrado['Estatus'] == 'Alerta Mecánica'])
c3.metric("Alertas Críticas Mecánicas 🚨", alertas, delta="Requiere Grúa" if alertas > 0 else "Normal", delta_color="inverse")
c4.metric("CSAT (Satisfacción Promedio)", f"{df_geo['Satisfaccion_Cliente'].mean():.1f} / 5.0")

st.divider()

col_mapa, col_datos = st.columns([2, 1])

with col_mapa:
    st.subheader("📍 Radar Georreferenciado Activo")
    # Mapeo avanzado usando st.map con soporte de colores semánticos
    st.map(
        df_filtrado,
        latitude="lat",
        longitude="lon",
        color="Color",
        size="Size",
        zoom=10,
        use_container_width=True
    )
    st.caption("🔴 Alerta Mecánica | 🟡 Demorado | 🔵 En Ruta | 🟢 Entregado (El tamaño del punto refleja el valor en US$)")

with col_datos:
    st.subheader("📊 Desempeño por Estatus")
    
    # Gráfico de Donut de Estatus
    chart = alt.Chart(df_filtrado).mark_arc(innerRadius=40).encode(
        theta=alt.Theta(field="Estatus", aggregate="count"),
        color=alt.Color(field="Estatus", type="nominal", scale=alt.Scale(
            domain=["Entregado", "En Ruta", "Demorado", "Alerta Mecánica"],
            range=["#22c55e", "#3b82f6", "#f59e0b", "#ef4444"]
        )),
        tooltip=['Estatus', 'count()']
    ).properties(height=280)
    st.altair_chart(chart, use_container_width=True)
    
    # Tabla de Top Conductores
    st.markdown("**🏆 Top Conductores (Efectividad)**")
    top_drivers = df_geo[df_geo["Estatus"] == "Entregado"].groupby("Conductor").size().sort_values(ascending=False).reset_index(name="Entregas Exitosas")
    st.dataframe(top_drivers, hide_index=True, use_container_width=True)
