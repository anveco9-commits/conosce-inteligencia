import pandas as pd
from sqlalchemy import create_engine

# URL CONOSCE
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
    "SECTOR / NIVEL DE GOBIERNO": "sector_nivel_gobierno",
    "SISTEMA_CONTRATACION": "sistema_contratacion",
    "TIPOPROCESOSELECCION": "tipo_proceso",
    "MONTOREFERENCIAL": "monto_referencial",
    "N_ITEM": "n_item",
    "DESCRIPCION_ITEM": "descripcion_item",
    "UNIDAD_MEDIDA": "unidad_medida",
    "ESTADOITEM": "estado_item",
    "PAQUETE": "paquete",
    "CODIGOITEM": "codigo_item_cubso",
    "ITEMCUBSO": "servicio",
    "MONTO_REFERENCIAL_ITEM": "monto_referencial_item",
    "MONEDA": "moneda",
    "DEPARTAMENTO_ITEM": "departamento_item",
    "PROVINCIA_ITEM": "provincia_item",
    "DISTRITO_ITEM": "distrito_item",
    "FECHA_CONVOCATORIA": "fecha_convocatoria",
    "FECHAINTEGRACIONBASES": "fecha_integracion",
    "FECHAPRESENTACIONPROPUESTA": "fecha_presentacion"
})

# Crear clave
df["clave_proceso_item"] = (
    df["codigo_convocatoria"].astype(str)
    + "-"
    + df["n_elemento"].astype(str)
)

# Mantener únicamente columnas existentes en PostgreSQL
columnas_destino = [
    "codigo_convocatoria",
    "entidad_ruc",
    "entidad",
    "objeto_contractual",
    "tipo_proceso",
    "servicio",
    "monto_referencial",
    "fecha_convocatoria",
    "fecha_integracion",
    "fecha_presentacion",
    "clave_proceso_item",
    "codigo_entidad",
    "tipo_entidad",
    "descripcion_proceso",
    "proceso",
    "tipo_compra",
    "sector_nivel_gobierno",
    "sistema_contratacion",
    "n_elemento",
    "descripcion_elemento",
    "unidad_medida",
    "estado_item",
    "paquete",
    "codigo_elemento",
    "moneda",
    "monto_elemento_referencial",
    "departamento_item",
    "provincia_item",
    "distrito_item"
]

df = df[columnas_destino]

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb"
)

# Vaciar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_convocatoria RESTART IDENTITY"
    )

# Cargar datos
df.to_sql(
    "fact_convocatoria",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("REGISTROS CARGADOS:", len(df))
