import re

html_code = """<!-- 08 · API DASHBOARD -->
<section id="dashboard-api" class="section-pad">
  <div class="container">
    <div class="cyber-river-card">
      <span class="section-kicker">// 08 · Dashboards Nivel PRO</span>
      <h2 class="section-title">Monitor de Mercados Financieros (API Global)</h2>
      <p class="lead-soft mt-2">
        Las instituciones financieras vigilan la volatilidad en tiempo real. Aquí conectaremos Python directamente a servidores de bolsa para extraer el histórico de divisas y cripto usando APIs reales.
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">La mesa de tesorería necesita vigilar el comportamiento del Dólar frente al Euro, la Libra y el Bitcoin para decidir coberturas, pero descargar reportes diarios en Excel es lento e ineficiente.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Usaremos la potente librería <code>yfinance</code> (Yahoo Finance) para conectarnos a la bolsa, extraer datos históricos (meses o años), y los graficaremos dinámicamente con <code>Altair</code>.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas yfinance altair</code>.</li>
          <li><strong>Crea un archivo:</strong> Copia el código de abajo y guárdalo como <code>app_api.py</code>.</li>
          <li><strong>Lanza el servidor:</strong> Ejecuta <code>python -m streamlit run app_api.py</code>.</li>
        </ol>
      </div>

      <div class="row mt-4">
        <div class="col-12">
          <h4 class="h5 mb-3 fw-bold text-primary"><i class="bi bi-code-square"></i> Código Fuente (app_api.py)</h4>
          <pre><code class="language-python">import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(page_title="Global Markets FX | API", layout="wide", page_icon="💹")

# ==============================================================================
# CONFIGURACIÓN Y OBTENCIÓN DE DATOS (API YFINANCE)
# ==============================================================================
st.sidebar.title("⚙️ Parámetros de Mercado")
moneda_base = st.sidebar.selectbox("Moneda Base:", ["USD", "EUR", "GBP"])
periodo = st.sidebar.select_slider("Período Histórico:", options=["5d", "1mo", "3mo", "6mo", "1y"], value="1mo")

PARES = {
    "EUR": f"{moneda_base}EUR=X",
    "GBP": f"{moneda_base}GBP=X",
    "JPY": f"{moneda_base}JPY=X",
    "MXN": f"{moneda_base}MXN=X",
    "BRL": f"{moneda_base}BRL=X",
    "BTC": f"BTC-{moneda_base}"
}

@st.cache_data(ttl=300) # Cache de 5 mins para no saturar la API
def extraer_datos_mercado(tickers, period):
    datos = {}
    for nombre, ticker in tickers.items():
        if moneda_base == nombre: continue # Evitar cruce igual
        try:
            hist = yf.Ticker(ticker).history(period=period)
            if not hist.empty:
                datos[nombre] = hist[['Close']].reset_index()
                datos[nombre]['Par'] = f"{moneda_base}/{nombre}"
        except:
            pass
    return datos

with st.spinner("Conectando con servidores de bolsa (Yahoo Finance)..."):
    mercado_data = extraer_datos_mercado(PARES, periodo)

# ==============================================================================
# PANEL PRINCIPAL
# ==============================================================================
st.title("💹 Tesorería Global & FX Tracker")
st.markdown("Cotizaciones en tiempo real e histórico de volatilidad de divisas.")

if mercado_data:
    st.markdown("### 📊 Tasas de Cambio Principales (Spot)")
    cols = st.columns(len(mercado_data))
    
    # Consolidar para gráfico
    dfs_lista = []
    
    for idx, (moneda, df_moneda) in enumerate(mercado_data.items()):
        # KPI y Variación
        ultimo_precio = df_moneda.iloc[-1]['Close']
        precio_previo = df_moneda.iloc[-2]['Close'] if len(df_moneda) > 1 else ultimo_precio
        variacion = ((ultimo_precio - precio_previo) / precio_previo) * 100
        
        # Color del KPI: En divisas (FX), si la tasa sube significa devaluación de la base, a menos que sea Crypto.
        cols[idx].metric(
            label=f"{moneda_base} / {moneda}", 
            value=f"{ultimo_precio:,.4f}", 
            delta=f"{variacion:.2f}%",
            delta_color="inverse" if moneda != "BTC" else "normal" 
        )
        
        # Preparar data para Altair
        df_limpio = df_moneda.copy()
        df_limpio['Moneda'] = moneda
        dfs_lista.append(df_limpio)

    df_consolidado = pd.concat(dfs_lista)
    
    st.divider()
    
    c1, c2 = st.columns([2,1])
    with c1:
        st.subheader("📈 Tendencia Histórica")
        # Grafico interactivo con Altair
        chart = alt.Chart(df_consolidado).mark_line(strokeWidth=3).encode(
            x=alt.X('Date:T', title='Fecha'),
            y=alt.Y('Close:Q', title='Tasa de Cambio', scale=alt.Scale(zero=False)),
            color=alt.Color('Moneda:N', legend=alt.Legend(orient="bottom")),
            tooltip=['Date:T', 'Moneda', 'Close']
        ).properties(height=400).interactive()
        st.altair_chart(chart, use_container_width=True)
        
    with c2:
        st.subheader("📋 Matriz de Datos")
        df_pivot = df_consolidado.pivot(index='Date', columns='Moneda', values='Close').sort_index(ascending=False).reset_index()
        df_pivot['Date'] = df_pivot['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_pivot, hide_index=True, use_container_width=True)
else:
    st.error("No se pudieron obtener datos de la API. Verifica tu conexión a Internet.")
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
      <h2 class="section-title">Análisis de Sentimiento (Motor NLP Avanzado)</h2>
      <p class="lead-soft mt-2">
        La minería de texto y el <strong>Procesamiento de Lenguaje Natural (NLP)</strong> extraen valor real de encuestas, redes sociales y correos electrónicos.
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">Atención al Cliente recibe miles de quejas (VoC - Voice of Customer) diarias por WhatsApp y Twitter. Leerlas a mano es inviable, y no detectan a tiempo las quejas urgentes o intentos de demanda.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Diseñaremos un <strong>Motor NLP de Categorización</strong> que detecta palabras clave, identifica el departamento responsable, calcula el nivel de riesgo (Crítico/Normal) y genera un plan de acción.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas altair</code>.</li>
          <li><strong>Crea un archivo:</strong> Copia el código de abajo y guárdalo como <code>app_nlp.py</code>.</li>
          <li><strong>Lanza el servidor:</strong> Ejecuta <code>python -m streamlit run app_nlp.py</code>.</li>
        </ol>
      </div>

      <!-- INSTRUCTIONS FOR NLP -->
      <div class="mt-4 mb-4 p-4 border rounded-3 bg-light">
        <h5 class="fw-bold"><i class="bi bi-vial-fill text-primary"></i> Datos de Prueba Interactiva (Copiar y Pegar en tu App)</h5>
        <p class="small text-secondary mb-3">Una vez tengas tu aplicación ejecutándose en el navegador, usa las opciones del <strong>menú lateral</strong> (Sidebar) y pega estos datos para ver la magia de tu motor NLP.</p>
        
        <ul class="nav nav-tabs mt-3" id="testTabs" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-telecom" type="button">Opción 1: Caso Telecom</button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-banco" type="button">Opción 2: Banca Digital</button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-csv" type="button">Opción 3: Carga Archivo CSV</button>
          </li>
        </ul>
        
        <div class="tab-content border border-top-0 p-3 bg-white" id="testTabsContent">
          <!-- TAB 1 -->
          <div class="tab-pane fade show active" id="tab-telecom">
            <p class="small text-secondary mb-2">Selecciona <strong>"3. Pegar Texto Masivo"</strong> en tu aplicación e ingresa esto:</p>
            <pre><code class="language-text">Excelente velocidad de internet de fibra óptica y el técnico llegó puntual, muy buen servicio y calidad.
Se cayó la señal en todo mi barrio, llevo dos días incomunicado y nadie contesta, una verdadera vergüenza.
Quisiera consultar cuándo es la fecha de vencimiento de mi factura de este mes y los medios de pago disponibles.
El servicio de atención no es bueno, la app móvil es muy lenta y se queda congelada al abrirla.
Me aplicaron un cobro indebido en la tarifa y me siguen debitando dinero tras cancelar, exijo solución o voy a denuncia.
El asesor por WhatsApp respondió muy rápido y fue muy amable, solucionó mi problema en minutos.</code></pre>
            <div class="alert alert-success py-2 mt-2 mb-0"><small><strong>¿Qué validará tu sistema?</strong><br>🟢 2 Positivos (Fibra y WhatsApp)<br>🟡 1 Neutro (Consulta operativa)<br>🔴 3 Negativos (Inversión por negación "no es bueno" y alertas CRÍTICAS por palabras como "incomunicado" y "denuncia").</small></div>
          </div>
          
          <!-- TAB 2 -->
          <div class="tab-pane fade" id="tab-banco">
             <p class="small text-secondary mb-2">Selecciona <strong>"3. Pegar Texto Masivo"</strong> en tu aplicación e ingresa esto:</p>
            <pre><code class="language-text">Me encanta la nueva actualización de la banca móvil, es súper fácil y rápido transferir dinero.
La app no me deja entrar desde la última actualización, da error de login constante y el soporte es pésimo.
¿Cuáles son los requisitos y el costo de mantenimiento para solicitar una tarjeta de crédito internacional?
Me cobraron cargos dobles en mi cuenta sin justificación, exijo la devolución inmediata de mi plata.
Excelente trato de la asesora en la sucursal, resolvió mi trámite con gran amabilidad y rapidez.</code></pre>
            <div class="alert alert-success py-2 mt-2 mb-0"><small><strong>¿Qué validará tu sistema?</strong><br>Detectará automáticamente los departamentos (App Móvil vs. Facturación vs. Atención al Cliente) y apilará gráficamente la proporción exacta verde/amarillo/rojo.</small></div>
          </div>
          
          <!-- TAB 3 -->
          <div class="tab-pane fade" id="tab-csv">
            <p class="small text-secondary mb-2">Selecciona <strong>"2. Subir Archivo (CSV)"</strong>, guarda este texto en tu PC como <code>opiniones.csv</code> y súbelo:</p>
            <pre><code class="language-text">ID,Canal,Cliente,Texto
CLI-01,Twitter,Laura Gomez,La fibra óptica vuela de rápido y nunca se cae, excelente calidad recomendada.
CLI-02,Call Center,Pedro Martinez,Pésima atención telefónica, estuve 40 minutos en espera y me cortan la llamada.
CLI-03,WhatsApp,Marta Ruiz,Hola buenas tardes, quisiera saber si tienen cobertura de internet en la zona norte.
CLI-04,App Store,Lucas Perez,La app no es rápida, se traba al querer ver la factura y tiene muchos errores.
CLI-05,Sucursal,Andres Castro,Excelente atención del equipo de soporte técnico, muy atentos y amables.
CLI-06,Twitter,Sofia Vega,Cancelé mi suscripción el mes pasado y me siguen debitando de la tarjeta, un desastre total.</code></pre>
            <div class="alert alert-success py-2 mt-2 mb-0"><small><strong>¿Qué validará tu sistema?</strong><br>La lectura inteligente de columnas y mostrará el gráfico de rendimiento por "Canal de Contacto" (Twitter vs App Store, etc).</small></div>
            <p class="small text-primary mt-2 mb-0"><i class="bi bi-download"></i> Una vez procesado, podrás descargar el reporte final limpio entrando a la pestaña <strong>"📋 Todos los Datos"</strong> y guardando tu <code>NLP_Analisis_Resultados.csv</code>.</p>
          </div>
        </div>
      </div>

      <div class="row mt-4">
        <div class="col-12">
          <h4 class="h5 mb-3 fw-bold text-primary"><i class="bi bi-code-square"></i> Código Fuente (app_nlp.py)</h4>
          <pre><code class="language-python">import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter
import re
import json
import io

# ==============================================================================
# CONFIGURACIÓN GENERAL
# ==============================================================================
st.set_page_config(
    page_title="Enterprise VoC Analytics | NLP Engine", 
    page_icon="📈", 
    layout="wide"
)

# Paleta de colores semántica empresarial
COLOR_SCALE = alt.Scale(
    domain=['Positivo', 'Neutro', 'Negativo'],
    range=['#22c55e', '#eab308', '#ef4444']  # Verde, Amarillo, Rojo
)

# ==============================================================================
# RECURSOS NLP Y REGLAS DE NEGOCIO
# ==============================================================================
STOPWORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si", "de", "en", 
    "para", "por", "con", "es", "son", "fue", "era", "su", "sus", "a", "al", "del", "que", "muy",
    "este", "esta", "estos", "estas", "como", "mi", "mis", "ha", "he", "ya", "me", "le", "les"
}

NEGACIONES = {"no", "tampoco", "nunca", "jamás", "nada", "sin", "ni"}

LEXICO_POS = {
    "excelente", "encanta", "rápido", "rapido", "genial", "buen", "bueno", "buena", "amable", 
    "atenta", "solucionaron", "impecable", "fácil", "perfecto", "calidad", "recomiendo", "gracias"
}

LEXICO_NEG = {
    "pésimo", "pesimo", "lenta", "lento", "malo", "mala", "error", "errores", "falla", "fallas", 
    "cobro", "estafa", "incomunicado", "cortan", "vergüenza", "engaño", "congelada", "caro", 
    "terrible", "desastre", "espera", "nunca", "inútil", "caído", "decepcionado"
}

CATEGORIAS_DEPARTAMENTO = {
    "Facturación y Cobranza": ["factura", "cobro", "cobron", "debitando", "tarifa", "precio", "saldo", "cargos", "plata", "pago"],
    "Red y Conectividad": ["señal", "5g", "fibra", "internet", "velocidad", "incomunicado", "router", "cae", "técnico", "tecnico", "cobertura"],
    "App Móvil y Plataforma": ["app", "aplicación", "transferir", "actualización", "web", "congelada", "interfaz", "login", "sistema", "error"],
    "Atención al Cliente": ["asesor", "asesora", "soporte", "atención", "atencion", "llamada", "whatsapp", "espera", "sucursal", "demora"]
}

TERMINOS_CRITICOS = {"estafa", "denuncia", "defensa del consumidor", "incomunicado", "cortan", "abuso", "cobro indebido", "fraude"}

# ==============================================================================
# MOTOR NLP CORE
# ==============================================================================
def tokenizar(texto: str) -> list:
    return re.findall(r'\\b[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+\\b', str(texto).lower())

def procesar_texto_unitario(row: dict) -> dict:
    texto = str(row.get("Texto", ""))
    tokens = tokenizar(texto)
    score = 0
    pos_encontradas = []
    neg_encontradas = []

    for i, w in enumerate(tokens):
        prev = tokens[i-1] if i > 0 else ""
        negada = prev in NEGACIONES

        if w in LEXICO_POS:
            if negada:
                score -= 1
                neg_encontradas.append(f"no {w}")
            else:
                score += 1
                pos_encontradas.append(w)
        elif w in LEXICO_NEG:
            if negada:
                score += 0.5
            else:
                score -= 1
                neg_encontradas.append(w)

    if score > 0:
        sentimiento = "Positivo"
    elif score < 0:
        sentimiento = "Negativo"
    else:
        sentimiento = "Neutro"

    # Clasificar departamento
    dept_asignado = "Consultas / General"
    for dept, keywords in CATEGORIAS_DEPARTAMENTO.items():
        if any(k in tokens for k in keywords):
            dept_asignado = dept
            break

    # Prioridad
    es_critico = any(t in texto.lower() for t in TERMINOS_CRITICOS) or (score <= -2)
    prioridad = "ALTA (Crítico)" if es_critico else ("MEDIA" if sentimiento == "Negativo" else "NORMAL")

    return {
        "ID": row.get("ID", f"TKT-{hash(texto)%10000:04d}"),
        "Canal": row.get("Canal", "Web / Ingesta"),
        "Cliente": row.get("Cliente", "Cliente Registrado"),
        "Texto": texto,
        "Sentimiento": sentimiento,
        "Score": score,
        "Departamento": dept_asignado,
        "Prioridad": prioridad,
        "Tokens_Pos": ", ".join(pos_encontradas),
        "Tokens_Neg": ", ".join(neg_encontradas)
    }

# ==============================================================================
# DATA DEMO BASE (TELECOM & BANCO)
# ==============================================================================
DEMO_DATA = [
    {"ID": "TKT-101", "Canal": "Twitter", "Cliente": "Carlos M.", "Texto": "Me cobraron el doble en la factura de este mes sin justificación. Pésimo soporte."},
    {"ID": "TKT-102", "Canal": "App Store", "Cliente": "Mariana G.", "Texto": "La señal 5G es increíblemente rápida en mi ciudad, me encanta la velocidad para trabajar."},
    {"ID": "TKT-103", "Canal": "Encuesta CSAT", "Cliente": "Jorge L.", "Texto": "La aplicación no me deja transferir dinero desde ayer, se queda congelada. Terrible falla."},
    {"ID": "TKT-104", "Canal": "Sucursal", "Cliente": "Camila R.", "Texto": "Excelente atención de la asesora en el centro de atención, fue muy amable y rápida."},
    {"ID": "TKT-105", "Canal": "Twitter", "Cliente": "Esteban D.", "Texto": "Se cae la señal cada vez que llueve. Llevo 3 días incomunicado, una verdadera vergüenza."},
    {"ID": "TKT-106", "Canal": "WhatsApp", "Cliente": "Lucía P.", "Texto": "¿Cuál es el horario de atención para consultar las tarifas de planes prepago?"},
    {"ID": "TKT-107", "Canal": "Call Center", "Cliente": "Roberto F.", "Texto": "Cancelé el plan hace 2 meses y me siguen debitando dinero. Exijo una solución inmediata o denuncia."},
    {"ID": "TKT-108", "Canal": "App Store", "Cliente": "Valeria H.", "Texto": "Muy buena la nueva actualización de la app, ahora es fácil y rápido ver consumos."},
    {"ID": "TKT-109", "Canal": "Call Center", "Cliente": "Andrés V.", "Texto": "El router vino con falla, prometieron técnico para hoy y nunca llegó al domicilio."},
    {"ID": "TKT-110", "Canal": "WhatsApp", "Cliente": "Sofía T.", "Texto": "El soporte por WhatsApp resolvió mi consulta en cinco minutos, muy atentos y rápida solución."},
    {"ID": "TKT-111", "Canal": "Encuesta CSAT", "Cliente": "Martín S.", "Texto": "Quisiera información sobre planes con roaming internacional para viajar el mes próximo."},
    {"ID": "TKT-112", "Canal": "Twitter", "Cliente": "Daniela B.", "Texto": "Me ofrecieron una promoción telefónica engañosa y me vino un cobro indebido. Pésimo engaño."},
    {"ID": "TKT-113", "Canal": "App Store", "Cliente": "Gonzalo C.", "Texto": "La acreditación del saldo demoró un poco pero al final funcionó normal."},
    {"ID": "TKT-114", "Canal": "Call Center", "Cliente": "Clara N.", "Texto": "El soporte telefónico te tiene 45 minutos en espera y luego te cortan la llamada."},
    {"ID": "TKT-115", "Canal": "Sucursal", "Cliente": "Mateo K.", "Texto": "Llevo 4 años con el servicio de fibra óptica y la calidad siempre ha sido impecable y excelente."}
]

# ==============================================================================
# BARRA LATERAL: FUENTES DE DATOS & PLANTILLAS
# ==============================================================================
st.sidebar.title("🗂️ Fuente de Datos")
origen = st.sidebar.radio(
    "Selecciona cómo cargar los datos:",
    ["1. Dataset Demo (Telecom/Banca)", "2. Subir Archivo (CSV, JSON, TXT)", "3. Pegar Texto Masivo"]
)

df_a_procesar = None

if origen == "1. Dataset Demo (Telecom/Banca)":
    df_a_procesar = pd.DataFrame(DEMO_DATA)
    st.sidebar.success(f"Cargados {len(df_a_procesar)} comentarios demo.")

elif origen == "2. Subir Archivo (CSV, JSON, TXT)":
    archivo = st.sidebar.file_uploader("Sube tu archivo de opiniones", type=["csv", "json", "txt"])
    
    # Botón para descargar plantilla de ejemplo para estudiantes
    csv_plantilla = pd.DataFrame(DEMO_DATA[:5]).to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("📄 Descargar Plantilla CSV Ejemplo", data=csv_plantilla, file_name="plantilla_feedback.csv", mime="text/csv")
    
    if archivo is not None:
        try:
            if archivo.name.endswith(".csv"):
                df_cargado = pd.read_csv(archivo)
            elif archivo.name.endswith(".json"):
                data_json = json.load(archivo)
                df_cargado = pd.DataFrame(data_json)
            elif archivo.name.endswith(".txt"):
                lineas = [l.strip() for l in archivo.read().decode("utf-8").split("\\n") if l.strip()]
                df_cargado = pd.DataFrame({"Texto": lineas})

            # Detectar o seleccionar la columna de texto
            columnas = df_cargado.columns.tolist()
            col_sugerida = next((c for c in columnas if c.lower() in ["texto", "feedback", "comentario", "review", "mensaje"]), columnas[0])
            col_elegida = st.sidebar.selectbox("Columna que contiene los textos:", columnas, index=columnas.index(col_sugerida))
            
            df_cargado = df_cargado.rename(columns={col_elegida: "Texto"})
            df_a_procesar = df_cargado
            st.sidebar.success(f"Cargados {len(df_a_procesar)} registros exitosamente.")
        except Exception as e:
            st.sidebar.error(f"Error al leer archivo: {e}")

elif origen == "3. Pegar Texto Masivo":
    st.sidebar.markdown("**Pega comentarios (uno por renglón):**")
    texto_pegado = st.sidebar.text_area("Lote de textos:", height=200, 
        value="El servicio de internet es muy malo y se corta siempre.\\nExcelente la atención por chat, solucionaron en minutos.\\nQuiero saber cuándo vence mi factura.\\nLa app móvil da error al loguearse, pésimo servicio.")
    
    if texto_pegado.strip():
        lineas = [l.strip() for l in texto_pegado.split("\\n") if l.strip()]
        df_a_procesar = pd.DataFrame({"Texto": lineas})
        st.sidebar.info(f"{len(lineas)} renglones detectados.")

# ==============================================================================
# PANTALLA PRINCIPAL
# ==============================================================================
st.title("🎯 Central de Inteligencia de Clientes (VoC Analytics)")
st.markdown("Análisis semántico automatizado, detección de quejas críticas y matriz de priorización operativa.")

if df_a_procesar is not None:
    c_btn, c_prev = st.columns([1, 4])
    with c_btn:
        ejecutar = st.button("🚀 Ejecutar Análisis NLP", type="primary", use_container_width=True)
    with c_prev:
        st.caption(f"Registros listos para procesar: **{len(df_a_procesar)}**")

    if ejecutar or "analisis_listo" in st.session_state:
        st.session_state["analisis_listo"] = True
        
        # Procesamiento
        data_dicts = df_a_procesar.to_dict(orient="records")
        resultado = [procesar_texto_unitario(row) for row in data_dicts]
        df_res = pd.DataFrame(resultado)

        # --------------------------------------------------------------------------
        # 1. KPIs EJECUTIVOS
        # --------------------------------------------------------------------------
        total = len(df_res)
        n_pos = len(df_res[df_res["Sentimiento"] == "Positivo"])
        n_neu = len(df_res[df_res["Sentimiento"] == "Neutro"])
        n_neg = len(df_res[df_res["Sentimiento"] == "Negativo"])
        n_crit = len(df_res[df_res["Prioridad"] == "ALTA (Crítico)"])
        nss = int(((n_pos - n_neg) / total) * 100) if total > 0 else 0

        st.divider()
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Volumen Analizado", f"{total}")
        k2.metric("Positivos 🟢", f"{n_pos} ({n_pos/total*100:.0f}%)" if total > 0 else "0")
        k3.metric("Neutros 🟡", f"{n_neu} ({n_neu/total*100:.0f}%)" if total > 0 else "0")
        k4.metric("Negativos 🔴", f"{n_neg} ({n_neg/total*100:.0f}%)" if total > 0 else "0")
        k5.metric("🚨 Casos Críticos", f"{n_crit}", delta="Alerta Churn" if n_crit > 0 else "Controlado", delta_color="inverse")

        # --------------------------------------------------------------------------
        # 2. GRÁFICOS ANALÍTICOS (CON COLORES SEMÁNTICOS EXACTOS)
        # --------------------------------------------------------------------------
        st.markdown("### 📊 Tablero de Control Visual")
        g1, g2 = st.columns([1, 1.4])

        with g1:
            st.subheader("1. Distribución Global de Sentimiento")
            df_conteo = df_res["Sentimiento"].value_counts().reset_index()
            df_conteo.columns = ["Sentimiento", "Total"]

            chart_sent = alt.Chart(df_conteo).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
                x=alt.X('Sentimiento:N', sort=['Positivo', 'Neutro', 'Negativo'], title=None),
                y=alt.Y('Total:Q', title='Cantidad de Comentarios'),
                color=alt.Color('Sentimiento:N', scale=COLOR_SCALE, legend=None),
                tooltip=['Sentimiento', 'Total']
            ).properties(height=320)

            st.altair_chart(chart_sent, use_container_width=True)

        with g2:
            st.subheader("2. Foco de Problemas por Departamento")
            chart_dept = alt.Chart(df_res).mark_bar().encode(
                y=alt.Y('Departamento:N', sort='-x', title='Área / Departamento'),
                x=alt.X('count():Q', stack='normalize', axis=alt.Axis(format='%'), title='Composición (%)'),
                color=alt.Color('Sentimiento:N', scale=COLOR_SCALE, title="Sentimiento"),
                tooltip=['Departamento', 'Sentimiento', 'count()']
            ).properties(height=320)

            st.altair_chart(chart_dept, use_container_width=True)

        # Gráfico adicional: Volumen por Canal
        if "Canal" in df_res.columns and df_res["Canal"].nunique() > 1:
            st.subheader("3. Rendimiento por Canal de Contacto")
            chart_canal = alt.Chart(df_res).mark_bar().encode(
                x=alt.X('Canal:N', title="Canal"),
                y=alt.Y('count():Q', title="Volumen"),
                color=alt.Color('Sentimiento:N', scale=COLOR_SCALE),
                tooltip=['Canal', 'Sentimiento', 'count()']
            ).properties(height=240)
            st.altair_chart(chart_canal, use_container_width=True)

        # --------------------------------------------------------------------------
        # 3. NAVEGACIÓN Y AUDITORÍA DE DATOS
        # --------------------------------------------------------------------------
        st.markdown("### 💬 Detalle de Opiniones y Planes de Acción")
        tab_neg, tab_pos, tab_neu, tab_todos, tab_mejoras = st.tabs([
            f"🔴 Negativos ({n_neg})", 
            f"🟢 Positivos ({n_pos})", 
            f"🟡 Neutros ({n_neu})", 
            "📋 Todos los Datos (Exportable)",
            "💡 Plan de Mejoras Sugeridas"
        ])

        with tab_neg:
            st.error("Comentarios de detractores requiriendo atención prioritaria:")
            df_neg = df_res[df_res["Sentimiento"] == "Negativo"][["ID", "Canal", "Departamento", "Prioridad", "Texto", "Tokens_Neg"]]
            st.dataframe(df_neg, use_container_width=True, hide_index=True)

        with tab_pos:
            st.success("Menciones de promotores (oportunidades para marketing y testimonios):")
            df_pos = df_res[df_res["Sentimiento"] == "Positivo"][["ID", "Canal", "Departamento", "Texto", "Tokens_Pos"]]
            st.dataframe(df_pos, use_container_width=True, hide_index=True)

        with tab_neu:
            st.warning("Consultas operativas o transaccionales sin carga emocional:")
            df_neu = df_res[df_res["Sentimiento"] == "Neutro"][["ID", "Canal", "Departamento", "Texto"]]
            st.dataframe(df_neu, use_container_width=True, hide_index=True)

        with tab_todos:
            st.dataframe(df_res[["ID", "Canal", "Cliente", "Departamento", "Sentimiento", "Prioridad", "Texto"]], use_container_width=True)
            csv_output = df_res.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Resultados Completos (CSV)", data=csv_output, file_name="NLP_Analisis_Resultados.csv", mime="text/csv")

        # --------------------------------------------------------------------------
        # 4. PLAN DE MEJORAS BASADO EN LOS DATOS DETECTADOS
        # --------------------------------------------------------------------------
        with tab_mejoras:
            st.subheader("🛠️ Matriz de Mejoras Operativas Sugeridas")
            
            dept_neg = df_res[df_res["Sentimiento"] == "Negativo"]["Departamento"].value_counts()
            top_problema = dept_neg.index[0] if not dept_neg.empty else "Ninguno"

            st.warning(f"**Área con mayor volumen de insatisfacción:** `{top_problema}` ({dept_neg.iloc[0] if not dept_neg.empty else 0} quejas)")

            c_rec1, c_rec2 = st.columns(2)
            with c_rec1:
                st.markdown('''
                #### 1. Facturación y Finanzas
                * **Diagnóstico:** Reclamos recurrentes por cobros posteriores a cancelaciones y tarifas engañosas.
                * **Solución de raíz:** Implementar confirmación de cancelación con token y congelamiento automático de débitos.
                * **KPI a impactar:** Reducción de 25% en llamadas a reclamos de cobranzas.

                #### 2. Canales Digitales y App
                * **Diagnóstico:** Incidencias en operaciones de transferencia y cuelgues del sistema.
                * **Solución de raíz:** Auditoría técnica en timeouts del API Gateway y monitor de estabilidad móvil.
                * **KPI a impactar:** Aumento en calificación de App Store / Play Store.
                ''')
            with c_rec2:
                st.markdown('''
                #### 3. Red y Cuadrillas Técnicas
                * **Diagnóstico:** Incumplimiento de visitas a domicilio e interrupción por clima.
                * **Solución de raíz:** Geocercas con tracking en tiempo real del técnico (estilo Uber) y alertas SMS proactivas.
                * **KPI a impactar:** Disminución del 40% en reclamos por citas técnicas perdidas.

                #### 4. Canales de Atención (Call Center vs Chat)
                * **Diagnóstico:** Esperas prolongadas en canal telefónico (más de 40 min).
                * **Solución de raíz:** Desviar tráfico simple al bot de WhatsApp y habilitar opción de llamada devuelta (*Callback*).
                * **KPI a impactar:** Reducción del TMO (Tiempo Medio de Operación).
                ''')
else:
    st.info("👈 Por favor selecciona una fuente de datos en el menú lateral para comenzar.")
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
      <h2 class="section-title">Logística & Supply Chain (GeoTracking 360)</h2>
      <p class="lead-soft mt-2">
        La visualización geoespacial es la columna vertebral del comercio electrónico, las flotas logísticas y el control de tráfico en tiempo real. 
      </p>

      <div class="row mt-4">
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-danger"><i class="bi bi-x-circle-fill"></i> El Reto de Negocio</h5>
            <p class="text-secondary small">Una compañía de distribución tiene más de 300 camiones rodando. Ver tablas de Excel con coordenadas no ayuda al gerente de operaciones a prever cuellos de botella ni identificar qué unidades tienen averías.</p>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="p-4 rounded-4" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <h5 class="fw-bold text-success"><i class="bi bi-check-circle-fill"></i> La Solución Python</h5>
            <p class="text-secondary small">Construiremos un <strong>Gemelo Digital Logístico</strong>. Usaremos mapas interactivos donde cada vehículo es un punto geolocalizado: el color indicará su estatus (Verde = Ok, Rojo = Avería) y el tamaño indicará el valor económico de su carga.</p>
          </div>
        </div>
      </div>

      <div class="alert alert-info border-0 shadow-sm mt-3" role="alert" style="background-color: rgba(13, 110, 253, 0.05);">
        <h5 class="alert-heading fw-bold"><i class="bi bi-tools"></i> Cómo ejecutar esto en tu VS Code local:</h5>
        <ol class="text-secondary mb-0">
          <li><strong>Instala las dependencias:</strong> En tu terminal ejecuta <code>python -m pip install streamlit pandas numpy altair</code>.</li>
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
import altair as alt

st.set_page_config(page_title="Supply Chain & Fleet Control", layout="wide", page_icon="🚚")

# ==============================================================================
# SIMULADOR DE GEMELO DIGITAL LOGÍSTICO (DATA SINTÉTICA)
# ==============================================================================
@st.cache_data
def generar_flota():
    np.random.seed(101)
    n_rutas = 300
    # Centro de Distribución (Base): Haina / Santo Domingo
    lat_base, lon_base = 18.4234, -70.0211 
    
    data = pd.DataFrame({
        "ID_Ruta": [f"RT-{i:04d}" for i in range(1, n_rutas+1)],
        "Vehiculo": np.random.choice(["Camión Frigorífico", "Furgón Ligero", "Moto Delivery"], n_rutas, p=[0.2, 0.5, 0.3]),
        "Conductor": np.random.choice(["Juan P.", "Miguel R.", "Luis S.", "Ana M.", "Carlos T."], n_rutas),
        "lat": np.random.normal(lat_base, 0.08, n_rutas),
        "lon": np.random.normal(lon_base, 0.08, n_rutas),
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
</code></pre>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- 11 · AGENDA DE 120 MINUTOS -->
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<!-- 08 · API DASHBOARD -->'
end_marker = '<!-- 11 · AGENDA DE 120 MINUTOS -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Replace the chunk
    new_content = content[:start_idx] + html_code + content[end_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Html replaced")
else:
    print("ERROR: Boundaries not found")
