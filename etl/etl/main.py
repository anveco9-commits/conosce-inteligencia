import pandas as pd

url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/convocatorias/2026/CONVOCATORIAS2026_0.xlsx"

df = pd.read_excel(
    url,
    engine="openpyxl"
)

print("FILAS:", len(df))
print("COLUMNAS:", len(df.columns))

print("COLUMNAS ENCONTRADAS:")
print(df.columns.tolist())
