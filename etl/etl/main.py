import requests
import pandas as pd
from io import BytesIO

url = "https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal/redirect.html/content?userid=public&password=key&url=aHR0cHM6Ly9jb25vc2NlLm9zY2UuZ29iLnBlL2J1c2NhZG9yL2Fzc2V0cy82N2FlNmM0YS9yZXBvcnRlcy9jb252b2NhdG9yaWFzLzIwMjYvQ09OVk9DQVRPUklBUzIwMjZfMC54bHN4"

respuesta = requests.get(url)
respuesta.raise_for_status()

excel_bytes = BytesIO(respuesta.content)

df = pd.read_excel(
    excel_bytes,
    engine="openpyxl"
)

print("FILAS:", len(df))
print("COLUMNAS:", len(df.columns))
print(df.columns.tolist())
