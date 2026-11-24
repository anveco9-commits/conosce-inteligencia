import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Convocatorias Cajamarca ya cargadas
convocatorias = pd.read_sql(
    """
    SELECT codigo_convocatoria
    FROM fact_convocatoria
    """,
    engine
)

# Archivo postores
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/postor/2026/POSTOR2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

# Renombrar columnas
df = df.rename(columns={
    "CODIGO_CONVOCATORIA": "codigo_convocatoria",
    "N_ITEM": "n_item",
    "RUC_CODIGO_POSTOR": "ruc_postor",
    "POSTOR": "postor",
    "FECHACONVOCATORIA": "fecha_convocatoria",
    "FECHA_PRESENTACION_PROPUESTA": "fecha_presentacion"
})

# Convertir tipos para hacer el cruce
df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)
convocatorias["codigo_convocatoria"] = convocatorias["codigo_convocatoria"].astype(str)

# Mantener solo procesos de Cajamarca
df = df.merge(
    convocatorias[["codigo_convocatoria"]],
    on="codigo_convocatoria",
    how="inner"
)

# Seleccionar columnas finales
df = df[
    [
        "codigo_convocatoria",
        "n_item",
        "ruc_postor",
        "postor",
        "fecha_convocatoria",
        "fecha_presentacion"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_postor RESTART IDENTITY"
    )

# Cargar datos
df.to_sql(
    "fact_postor",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("POSTORES CARGADOS:", len(df))
