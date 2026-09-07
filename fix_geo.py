with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """    # Centro de Distribución (Base): Haina / Santo Domingo
    lat_base, lon_base = 18.4234, -70.0211 
    
    data = pd.DataFrame({
        "ID_Ruta": [f"RT-{i:04d}" for i in range(1, n_rutas+1)],
        "Vehiculo": np.random.choice(["Camión Frigorífico", "Furgón Ligero", "Moto Delivery"], n_rutas, p=[0.2, 0.5, 0.3]),
        "Conductor": np.random.choice(["Juan P.", "Miguel R.", "Luis S.", "Ana M.", "Carlos T."], n_rutas),
        "lat": np.random.normal(lat_base, 0.08, n_rutas),
        "lon": np.random.normal(lon_base, 0.08, n_rutas),"""

replacement = """    # Centro de Distribución: Distrito Nacional (tierra firme)
    lat_base, lon_base = 18.4800, -69.9300 
    
    data = pd.DataFrame({
        "ID_Ruta": [f"RT-{i:04d}" for i in range(1, n_rutas+1)],
        "Vehiculo": np.random.choice(["Camión Frigorífico", "Furgón Ligero", "Moto Delivery"], n_rutas, p=[0.2, 0.5, 0.3]),
        "Conductor": np.random.choice(["Juan P.", "Miguel R.", "Luis S.", "Ana M.", "Carlos T."], n_rutas),
        "lat": np.random.normal(lat_base, 0.02, n_rutas), # Reducida la desviación para no caer al mar
        "lon": np.random.normal(lon_base, 0.02, n_rutas),"""

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Geo coordinates fixed.')
else:
    print('Target string not found in index.html')
