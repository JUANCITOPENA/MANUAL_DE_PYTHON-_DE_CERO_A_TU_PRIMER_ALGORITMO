# 🚀 Estatus del Proyecto: Manual de Python de Cero a tu Primer Algoritmo (V2 - Nivel Empresarial)

**Última actualización:** 05 de Septiembre 2026
**Estatus:** 🟢 Estable y Funcional al 100%

## 📋 Cambios Realizados (Mega Update Nivel PRO)

Se implementaron mejoras de nivel empresarial a la sección final del manual introduciendo 3 Dashboards PRO totalmente funcionales:

1. **Dashboard 1: Tesorería Global & FX Tracker (app_api.py)**
   - Sustituida la API inicial por **`yfinance`** para acceder a datos de la bolsa de valores real (Yahoo Finance).
   - Solucionado el problema de la zona horaria (`Tz-aware datetime`) de Pandas forzando a `utc=True`.
   - Incluye cotizaciones en vivo y datos históricos del Peso Dominicano (**DOP**), Euro, Libra Esterlina y Bitcoin.
   - Implementa gráficos de líneas con **Altair** para detectar volatilidad de mercado.

2. **Dashboard 2: Central de Inteligencia NLP (app_nlp.py)**
   - Motor de NLP (Natural Language Processing) para Voice of Customer (VoC).
   - Inyección del código ultra-profesional (incluye detección de semántica, negaciones como "no es bueno", stopwords, etc.).
   - Interfaz con TABS interactivos dentro del manual web (`index.html`) para que los alumnos copien los datos de prueba (Telecom, Banco Digital y CSV).
   - Gráficos apilados de semántica de colores (Verde, Amarillo, Rojo).

3. **Dashboard 3: Centro de Operaciones GeoTracking 360 (app_geo.py)**
   - Simulador "Gemelo Digital" de una flota de 300 camiones rodando en República Dominicana.
   - Centro logístico anclado correctamente al **Distrito Nacional** (`18.4800, -69.9300`) y con desviación estándar reducida a `0.02` para asegurar que los camiones caigan en tierra firme (evitando el Mar Caribe).
   - Puntos geolocalizados en el mapa (`st.map()`) que cambian de color según el estatus (Alerta Mecánica = Rojo, En Ruta = Azul) y tamaño según el valor de la carga.
   - Barra lateral (Control Tower) para filtrar vehículos afectados.

## 🛠️ Tecnologías y Dependencias del Entorno Virtual (.venv)
- `streamlit` (UI Web interactiva)
- `pandas`, `numpy` (Manejo de datos vectoriales)
- `altair` (Gráficos estadísticos declarativos)
- `yfinance` (Ingesta de APIs del mercado de valores)

## 📌 Siguientes Pasos (Para el Estudiante / Docente)
- [x] Ejecutar la App: `python -m streamlit run app_api.py` (o cualquiera de los 3).
- [x] Se generó el archivo `NLP_Analisis_Resultados.csv` como plantilla base en Descargas.
- [ ] Listo para despliegue (Deployment) si se desea publicar en Streamlit Community Cloud.
