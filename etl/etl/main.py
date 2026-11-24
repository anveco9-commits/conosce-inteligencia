import pandas as pd
from sqlalchemy import create_engine

# Convocatorias Cajamarca ya cargadas
convocatorias = pd.read_sql(
    """
    SELECT codigo_convocatoria,
           clave_proceso_item
    FROM fact_convocatoria
    """,
    create_engine(
        "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb"
    )
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

df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)

convocatorias["codigo_convocatoria"] = (
    convocatorias["codigo_convocatoria"].astype(str)
)
# Mantener solo Cajamarca
df = df.merge(
    convocatorias[["codigo_convocatoria"]],
    on="codigo_convocatoria",
    how="inner"
)

print("POSTORES CAJAMARCA:", len(df))
