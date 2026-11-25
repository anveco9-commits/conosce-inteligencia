import pandas as pd

url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/adjudicaciones/2026/ADJUDICACIONES2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print("FILAS:", len(df))
print("COLUMNAS:", len(df.columns))
print(df.columns.tolist())
