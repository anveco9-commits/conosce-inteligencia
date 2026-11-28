import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Convocatorias Cajamarca
convocatorias = pd.read_sql(
    """
    SELECT
        codigo_convocatoria,
        entidad,
        descripcion_proceso,
        provincia_item,
        distrito_item
    FROM fact_convocatoria
    """,
    engine
)

# Archivo contrataciones directas
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/adjudicaciones/2026/ADJUDICACIONES_CD2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print(df.columns.tolist())

# Renombrar columnas principales
df = df.rename(columns={
    "CODIGOCONVOCATORIA": "codigo_convocatoria",
    "RUC PROVEEDOR": "ruc_proveedor",
    "PROVEEDOR": "proveedor",
    "MONTO_ADJUDICADO_ITEM_SOLES": "monto_adjudicado",
    "FECHA_BUENAPRO": "fecha_buenapro"
})

# Convertir
df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)
convocatorias["codigo_convocatoria"] = convocatorias["codigo_convocatoria"].astype(str)

# Filtrar Cajamarca
df = df.merge(
    convocatorias,
    on="codigo_convocatoria",
    how="inner"
)

# Fecha
if "fecha_buenapro" in df.columns:
    df["fecha_buenapro"] = pd.to_datetime(
        df["fecha_buenapro"],
        dayfirst=True,
        errors="coerce"
    )

# Columnas por defecto
for col in [
    "ruc_proveedor",
    "proveedor",
    "monto_adjudicado",
    "fecha_buenapro"
]:
    if col not in df.columns:
        df[col] = None

# Estructura final
df = df[
    [
        "codigo_convocatoria",
        "entidad",
        "descripcion_proceso",
        "provincia_item",
        "distrito_item",
        "ruc_proveedor",
        "proveedor",
        "monto_adjudicado",
        "fecha_buenapro"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_contratacion_directa RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_contratacion_directa",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("CONTRATACIONES DIRECTAS CARGADAS:", len(df))
