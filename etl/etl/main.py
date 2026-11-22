import requests

url = "https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal/redirect.html/content?userid=public&password=key&url=aHR0cHM6Ly9jb25vc2NlLm9zY2UuZ29iLnBlL2J1c2NhZG9yL2Fzc2V0cy82N2FlNmM0YS9yZXBvcnRlcy9jb252b2NhdG9yaWFzLzIwMjYvQ09OVk9DQVRPUklBUzIwMjZfMC54bHN4"

archivo = "convocatorias2026.xlsx"

respuesta = requests.get(url)

with open(archivo, "wb") as f:
    f.write(respuesta.content)

print("Archivo descargado correctamente")
