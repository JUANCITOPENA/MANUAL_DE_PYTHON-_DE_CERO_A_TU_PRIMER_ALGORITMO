import re

html_to_inject = '''<!-- 08 · API DASHBOARD -->
<section id="dashboard-api" class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 08 · Dashboards Nivel PRO</span>
      <h2 class="section-title">Monitor de Divisas en Tiempo Real (API)</h2>
      <p class="lead-soft mt-2">
        Las empresas multinacionales necesitan vigilar los mercados. Aquí conectaremos Python directamente al internet para extraer tipos de cambio en vivo usando APIs públicas.
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">Revisar los tipos de cambio manualmente en el banco central todos los días es lento y propenso a errores. Finanzas necesita un monitor automático que se actualice solo.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Usaremos la librería <code>requests</code> para conectarnos a una <strong>API REST pública</strong>, extraer los datos en formato JSON, convertirlos a Pandas y visualizarlos en Streamlit.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas requests</code>.</li>
          <li><strong>Crea un archivo:</strong> Copia el código de abajo y guárdalo como <code>app_api.py</code>.</li>
          <li><strong>Lanza el servidor:</strong> Ejecuta <code>python -m streamlit run app_api.py</code>.</li>
        </ol>
      </div>

      <div class="row mt-4">
        <div class="col-12">
          <h4 class="h5 mb-3 fw-bold text-primary"><i class="bi bi-code-square"></i> Código Fuente (app_api.py)</h4>
          <pre><code class="language-python">import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor Global API", layout="wide")
st.title("🌍 Monitor de Divisas en Tiempo Real")
st.caption("Conectado a APIs Públicas - Ing. Juancito Peña")

@st.cache_data(ttl=600)
def obtener_datos_api():
    # Llamada a API pública de tipos de cambio
    url_fiat = "https://api.exchangerate-api.com/v4/latest/USD"
    res_fiat = requests.get(url_fiat).json()
    tasas = res_fiat["rates"]
    
    df_tasas = pd.DataFrame(list(tasas.items()), columns=["Moneda", "Valor por 1 USD"])
    return df_tasas

try:
    df = obtener_datos_api()
    
    st.subheader("Tasas de Cambio vs Dólar (USD)")
    
    # Filtros de las monedas más comunes
    monedas_clave = ["EUR", "DOP", "MXN", "GBP", "JPY", "COP", "CLP"]
    df_filtrado = df[df["Moneda"].isin(monedas_clave)].sort_values("Valor por 1 USD")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Euro (EUR)", f"€ {float(df[df['Moneda']=='EUR']['Valor por 1 USD']):.2f}")
    c2.metric("Peso Dom (DOP)", f"RD$ {float(df[df['Moneda']=='DOP']['Valor por 1 USD']):.2f}")
    c3.metric("Peso Mex (MXN)", f"MXN$ {float(df[df['Moneda']=='MXN']['Valor por 1 USD']):.2f}")
    
    st.divider()
    
    c_grafico, c_tabla = st.columns([2, 1])
    with c_grafico:
        st.bar_chart(df_filtrado.set_index("Moneda"))
    with c_tabla:
        st.dataframe(df_filtrado, width="stretch")
    
except Exception as e:
    st.error(f"Error de conexión con la API: {e}")
</code></pre>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- 09 · NLP DASHBOARD -->
<section id="dashboard-nlp" class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 09 · Dashboards Nivel PRO</span>
      <h2 class="section-title">Análisis de Sentimiento (NLP Básico)</h2>
      <p class="lead-soft mt-2">
        La minería de texto y el análisis de lenguaje natural (NLP) permiten extraer valor de datos no estructurados, como comentarios de clientes o noticias de internet.
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">Marketing recibe miles de encuestas de satisfacción. Leerlas una por una es imposible y no arroja datos cuantitativos sobre cómo se siente el cliente realmente.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Crearemos un algoritmo heurístico que limpia el texto, cuenta palabras clave (frecuencia) y determina si el mensaje es Positivo o Negativo al instante usando conteo matemático.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas</code>.</li>
          <li><strong>Crea un archivo:</strong> Copia el código de abajo y guárdalo como <code>app_nlp.py</code>.</li>
          <li><strong>Lanza el servidor:</strong> Ejecuta <code>python -m streamlit run app_nlp.py</code>.</li>
        </ol>
      </div>

      <div class="row mt-4">
        <div class="col-12">
          <h4 class="h5 mb-3 fw-bold text-primary"><i class="bi bi-code-square"></i> Código Fuente (app_nlp.py)</h4>
          <pre><code class="language-python">import streamlit as st
import pandas as pd
from collections import Counter
import re

st.set_page_config(page_title="Text Analytics NLP", layout="wide")
st.title("🧠 Analizador de Sentimiento y Text Mining")
st.caption("Minería de datos no estructurados - Ing. Juancito Peña")

st.markdown("Escribe o pega aquí las opiniones de tus clientes para extraer el **ADN del texto**.")

texto_usuario = st.text_area("Feedback del cliente:", 
    "El servicio es excelente, me encanta la plataforma. Sin embargo, la app móvil es un poco lenta y necesita mejorar. Pero en general, excelente soporte técnico y muy rápido.")

if st.button("Ejecutar Análisis NLP"):
    with st.spinner("Procesando redes lingüísticas..."):
        # 1. Limpieza (Regex para dejar solo letras)
        palabras = re.findall(r'\b[a-zA-ZáéíóúñÁÉÍÓÚÑ]+\b', texto_usuario.lower())
        
        # 2. Filtrado de Stopwords (Palabras vacías)
        stopwords = {"el", "la", "los", "las", "un", "una", "y", "o", "pero", "si", "de", "en", "para", "por", "con", "es", "su", "a", "que", "un", "poco"}
        palabras_limpias = [p for p in palabras if p not in stopwords and len(p) > 2]
        
        # 3. Conteo de Frecuencia
        frecuencia = Counter(palabras_limpias)
        df_freq = pd.DataFrame(frecuencia.most_common(10), columns=["Palabra", "Frecuencia"])
        
        # 4. Sentimiento Básico (Diccionarios Heurísticos)
        positivas = {"excelente", "encanta", "mejorar", "bueno", "genial", "rápido"}
        negativas = {"lenta", "mala", "pésimo", "peor", "error", "falla"}
        
        score_pos = sum(1 for p in palabras_limpias if p in positivas)
        score_neg = sum(1 for p in palabras_limpias if p in negativas)
        
        # Visualización
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Frecuencia de Palabras Clave")
            st.bar_chart(df_freq.set_index("Palabra"), color="#8b5cf6")
            
        with c2:
            st.subheader("Termómetro de Sentimiento")
            if score_pos > score_neg:
                st.success(f"Positivo 🟢 (Score: +{score_pos - score_neg})")
            elif score_neg > score_pos:
                st.error(f"Negativo 🔴 (Score: {score_pos - score_neg})")
            else:
                st.warning("Neutro 🟡 (Balanceado o sin datos)")
                
            st.metric("Total Palabras Válidas Analizadas", len(palabras_limpias))
            st.dataframe(df_freq, width="stretch")
</code></pre>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- 10 · LOGISTICA Y MAPAS -->
<section id="dashboard-geo" class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 10 · Dashboards Nivel PRO</span>
      <h2 class="section-title">Logística & GeoTracking 360</h2>
      <p class="lead-soft mt-2">
        La visualización geoespacial es fundamental para cadenas de suministro, delivery y ruteo estratégico. Streamlit nos permite graficar coordenadas masivas en milisegundos.
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">Tenemos cientos de envíos distribuidos en el país. Mirar una tabla de Excel con direcciones no ayuda a los supervisores de logística a entender la saturación de las zonas.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Usaremos coordenadas (Latitud y Longitud) junto con <code>st.map()</code> para renderizar puntos interactivos sobre un mapa satelital al instante de manera visual y clara.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas numpy</code>.</li>
          <li><strong>Crea un archivo:</strong> Copia el código de abajo y guárdalo como <code>app_geo.py</code>.</li>
          <li><strong>Lanza el servidor:</strong> Ejecuta <code>python -m streamlit run app_geo.py</code>.</li>
        </ol>
      </div>

      <div class="row mt-4">
        <div class="col-12">
          <h4 class="h5 mb-3 fw-bold text-primary"><i class="bi bi-code-square"></i> Código Fuente (app_geo.py)</h4>
          <pre><code class="language-python">import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="GeoTracking Logística", layout="wide")
st.title("📍 Control de Flotas y Logística 360")
st.caption("Mapeo de Rutas y Cobertura Dinámica - Ing. Juancito Peña")

# Generar datos geográficos simulados para Santo Domingo (Lat: 18.4861, Lon: -69.9312)
@st.cache_data
def generar_rutas():
    np.random.seed(42)
    puntos = 150
    df_geo = pd.DataFrame({
        "lat": np.random.normal(18.4861, 0.03, puntos),
        "lon": np.random.normal(-69.9312, 0.03, puntos),
        "Estado": np.random.choice(["Entregado", "En Tránsito", "Retrasado"], puntos, p=[0.7, 0.2, 0.1]),
        "Vehiculo": np.random.choice(["Camión A", "Camión B", "Moto C", "Van D"], puntos)
    })
    return df_geo

df = generar_rutas()

st.subheader("Mapa de Cobertura y Puntos de Entrega (Santo Domingo)")

# Filtros Dinámicos
vehiculo_sel = st.selectbox("Filtrar por Unidad Móvil:", ["Todos"] + list(df["Vehiculo"].unique()))

if vehiculo_sel != "Todos":
    df_filtrado = df[df["Vehiculo"] == vehiculo_sel]
else:
    df_filtrado = df

c1, c2 = st.columns([2, 1])

with c1:
    # Streamlit mapea automáticamente si hay columnas 'lat' y 'lon'
    st.map(df_filtrado, zoom=11, size=15)
    
with c2:
    st.subheader("Estatus de Entregas")
    resumen = df_filtrado["Estado"].value_counts().reset_index()
    resumen.columns = ["Estado", "Cantidad"]
    
    entregados = len(df_filtrado[df_filtrado['Estado'] == 'Entregado'])
    total = len(df_filtrado)
    
    st.metric("Eficiencia de Ruta", f"{(entregados/total)*100:.1f}%")
    st.dataframe(resumen, width="stretch")
</code></pre>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- 11 · AGENDA DE 120 MINUTOS -->
<section class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 11 · Estructura Pedagógica</span>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''<!-- 08 · AGENDA DE 120 MINUTOS -->
<section class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 08 · Estructura Pedagógica</span>'''

if target in content:
    new_content = content.replace(target, html_to_inject)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")
