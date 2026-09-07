with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '''        # Forzar formato fecha (pd.to_datetime) para evitar AttributeError
        df_pivot['Date'] = pd.to_datetime(df_pivot['Date']).dt.strftime('%Y-%m-%d')'''

replacement = '''        # Convertir a datetime y forzar zona horaria UTC para evitar el error Tz-aware de yfinance
        df_pivot['Date'] = pd.to_datetime(df_pivot['Date'], utc=True).dt.strftime('%Y-%m-%d')'''

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Timezone bug fixed.')
else:
    print('Target string not found in index.html')
