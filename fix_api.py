with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_dict = '''PARES = {
    "EUR": f"{moneda_base}EUR=X",
    "GBP": f"{moneda_base}GBP=X",
    "JPY": f"{moneda_base}JPY=X",
    "MXN": f"{moneda_base}MXN=X",
    "BRL": f"{moneda_base}BRL=X",
    "BTC": f"BTC-{moneda_base}"
}'''

new_dict = '''PARES = {
    "EUR": f"{moneda_base}EUR=X",
    "GBP": f"{moneda_base}GBP=X",
    "DOP": f"{moneda_base}DOP=X",  # Peso Dominicano
    "MXN": f"{moneda_base}MXN=X",
    "BTC": f"BTC-{moneda_base}"
}'''

target_date = '''        df_pivot = df_consolidado.pivot(index='Date', columns='Moneda', values='Close').sort_index(ascending=False).reset_index()
        df_pivot['Date'] = df_pivot['Date'].dt.strftime('%Y-%m-%d')'''

new_date = '''        df_pivot = df_consolidado.pivot(index='Date', columns='Moneda', values='Close').sort_index(ascending=False).reset_index()
        # Forzar formato fecha (pd.to_datetime) para evitar AttributeError
        df_pivot['Date'] = pd.to_datetime(df_pivot['Date']).dt.strftime('%Y-%m-%d')'''

if target_dict in html:
    html = html.replace(target_dict, new_dict)
    print("Dict replaced.")
if target_date in html:
    html = html.replace(target_date, new_date)
    print("Date bug fixed.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
