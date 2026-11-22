import pandas as pd
from sqlalchemy import create_engine

# Archivo CONOSCE
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/convocatorias/2026/CONVOCATORIAS2026_0.xlsx"

# Leer Excel
df = pd.read_excel(url, engine="openpyxl")

# Renombrar columnas
df = df.rename(columns={
    "CODIGOENTIDAD": "codigo_entidad",
    "ENTIDAD_RUC": "entidad_ruc",
    "ENTIDAD": "entidad",
    "TIPOENTIDAD": "tipo_entidad",
    "CODIGOCONVOCATORIA": "codigo_convocatoria",
    "DESCRIPCION_PROCESO": "descripcion_proceso",
    "PROCESO": "proceso",
    "TIPOCOMPRA": "tipo_compra",
    "OBJETOCONTRACTUAL": "objeto_contractual",
    "SISTEMA_CONTRATACION": "sistema_contratacion",
    "N_ITEM": "n_item",
    "DESCRIPCION_ITEM": "descripcion_item",
    "UNIDAD_MEDIDA": "unidad_medida",
    "ESTADOITEM": "estado_item",
    "PAQUETE": "paquete",
    "CODIGOITEM": "codigo_item",
    "MONEDA": "moneda",
    "DEPARTAMENTO_ITEM": "departamento_item",
    "PROVINCIA_ITEM": "provincia_item",
    "DISTRITO_ITEM": "distrito_item"
})

# Conexion Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb"
)

# Carga
df.to_sql(
    "fact_convocatoria",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("REGISTROS CARGADOS:", len(df))
