import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Convocatorias Cajamarca
convocatorias = pd.read_sql(
    """
    SELECT codigo_convocatoria
    FROM fact_convocatoria
    """,
    engine
)

# Archivo adjudicaciones
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/adjudicaciones/2026/ADJUDICACIONES2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

# Renombrar columnas
df = df.rename(columns={
    "CODIGOCONVOCATORIA": "codigo_convocatoria",
    "N_ITEM": "n_elemento",
    "RUC PROVEEDOR": "ruc_ganador",
    "PROVEEDOR": "proveedor_ganador",
    "MONTO_ADJUDICADO_ITEM_SOLES": "monto_adjudicado",
    "FECHA_BUENAPRO": "fecha_buena_pro"
})

# Filtrar Cajamarca
df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)
convocatorias["codigo_convocatoria"] = convocatorias["codigo_convocatoria"].astype(str)

df = df.merge(
    convocatorias,
    on="codigo_convocatoria",
    how="inner"
)

# Crear clave
df["clave_proceso_item"] = (
    df["codigo_convocatoria"].astype(str)
    + "-"
    + df["n_elemento"].astype(str)
)

# Mantener solo columnas existentes en PostgreSQL
df = df[
    [
        "codigo_convocatoria",
        "n_elemento",
        "ruc_ganador",
        "proveedor_ganador",
        "monto_adjudicado",
        "fecha_buena_pro",
        "clave_proceso_item"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_adjudicacion RESTART IDENTITY"
    )

# Cargar datos
df.to_sql(
    "fact_adjudicacion",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("ADJUDICACIONES CARGADAS:", len(df))
