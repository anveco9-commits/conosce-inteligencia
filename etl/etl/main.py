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

# Archivo contratos
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/contratos/2026/CONTRATOS2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print(df.columns.tolist())

# Renombrar
df = df.rename(columns={
    "CODIGOCONVOCATORIA": "codigo_convocatoria"
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

# Campos por defecto
if "monto_contrato" not in df.columns:
    df["monto_contrato"] = None

if "fecha_contrato" not in df.columns:
    df["fecha_contrato"] = None

if "proveedor" not in df.columns:
    df["proveedor"] = None

if "ruc_proveedor" not in df.columns:
    df["ruc_proveedor"] = None

# Estructura final
df = df[
    [
        "codigo_convocatoria",
        "entidad",
        "descripcion_proceso",
        "provincia_item",
        "distrito_item",
        "monto_contrato",
        "fecha_contrato",
        "proveedor",
        "ruc_proveedor"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_contrato RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_contrato",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("CONTRATOS CARGADOS:", len(df))
