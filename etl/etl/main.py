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
    "N_ITEM": "n_item",
    "RUC PROVEEDOR": "ruc_proveedor",
    "PROVEEDOR": "proveedor",
    "MONTO_REFERENCIAL_ITEM_SOLES": "monto_referencial_item_soles",
    "MONTO_ADJUDICADO_ITEM_SOLES": "monto_adjudicado_item_soles",
    "FECHA_CONVOCATORIA": "fecha_convocatoria",
    "FECHA_BUENAPRO": "fecha_buenapro",
    "FECHA_CONSENTIMIENTO_BP": "fecha_consentimiento_bp"
})

# Filtrar Cajamarca
df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)
convocatorias["codigo_convocatoria"] = convocatorias["codigo_convocatoria"].astype(str)

df = df.merge(
    convocatorias,
    on="codigo_convocatoria",
    how="inner"
)

# Columnas finales
df = df[
    [
        "codigo_convocatoria",
        "n_item",
        "ruc_proveedor",
        "proveedor",
        "monto_referencial_item_soles",
        "monto_adjudicado_item_soles",
        "fecha_convocatoria",
        "fecha_buenapro",
        "fecha_consentimiento_bp"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_adjudicacion RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_adjudicacion",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("ADJUDICACIONES CARGADAS:", len(df))
