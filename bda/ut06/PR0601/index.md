# PR0601: Capa bronce en Amazon AWS

## Conexión
```python
import boto3
import requests
from requests.exceptions import Timeout, RequestException
import json
import pandas as pd
import datetime
try:
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    print("¡Conexión exitosa!")
    print(f"Tienes {len(buckets['Buckets'])} buckets en tu cuenta.")
except Exception as e:
    print("Error en la conexión. Revisa tus credenciales.")
    print(e)
```
```python
¡Conexión exitosa!
Tienes 3 buckets en tu cuenta.
```

## API
```python
bucket = "bronce-guille"

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYWZhZDUyMjM5QG5hemlzYXQuY29tIiwianRpIjoiNDJlNjc3NGItM2YwMS00MTRhLWJjOGMtODMxM2EzMjAyYTA0IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NzU1ODgyNDIsInVzZXJJZCI6IjQyZTY3NzRiLTNmMDEtNDE0YS1iYzhjLTgzMTNhMzIwMmEwNCIsInJvbGUiOiIifQ.h5ou35hc2ocGQQeEZjU3Z8E4AHc0t7lQKQ3PGORYO5U"
```

## Leemos el dataset
```python
def df_playas():
    df_playas = pd.read_csv(
        "playas_espanolas.csv",
        usecols = ["Nombre", "Provincia", "Término_M", "Duchas", "Aseos", "Acceso_dis", "Bandera_az", "X", "Y", "Grado_ocup", "Grado_urba"]
    )

    print("CSV playas leído.")
    return df_playas
```

## Obtenemos los datos de AEMET
```python
def datos_aemet(df_playas):
    provincias = set(df_playas["Provincia"].unique())
    endpoint = "/api/prediccion/provincia/hoy/"
    query_string = {"api_key": API_KEY}
    
    with open("codigos_provincias.json") as f:
        codigos_provincias = json.load(f)

    datos_aemet = ""
    for provincia in provincias:
        codigo = codigos_provincias[provincia]
    
        url = BASE_URL + endpoint + codigo
        try:
            response = requests.get(url, params = query_string, timeout = (3, 10))
            response.raise_for_status()
            response_json = response.json()
        
            datos = response_json.get("datos", None)
        
            if datos:
                response_provincia = requests.get(datos, timeout = (3, 10)).text

                datos_aemet = datos_aemet + "\n" + response_provincia
        except Timeout:
            print("ERROR: El servidor tardó demasiado en responder.")
        except RequestException as e:
            print(f"ERROR: {e}")

    print("AEMET: datos obtenidos.")
    return datos_aemet
```

## Subimos los datos
```python
def subida_datos(s3, bucket, ruta, datos):
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    existe_bucket = bucket in buckets

    if not existe_bucket:
        s3.create_bucket(Bucket = bucket)
    s3.upload_file(datos, bucket, ruta)
    print(f"Dataframe subido a s3://{bucket}/{ruta}")
```

## Subimos texto
```python
def subida_texto(s3, bucket, ruta, texto):
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    existe_bucket = bucket in buckets

    if not existe_bucket:
        s3.create_bucket(Bucket = bucket)
    
    s3.put_object(
            Bucket = bucket,
            Key = ruta,
            Body = texto.encode('utf-8')
        )
    print(f"Texto subido a s3://{bucket}/{ruta}")
```

## Ejecutamos todas las funciones
```python
df_playas = df_playas()
datos_aemet = datos_aemet(df_playas)
fecha_actual = datetime.datetime.now()

df_playas.to_csv("df_playas.csv")

subida_datos(s3, BUCKET, "bronce-guille/catalogos/guia_playas/v1/playas.csv", "df_playas.csv")
subida_texto(s3, BUCKET, f"bronce-guille/meteorologia/prediccion_playas/{fecha_actual.year}/{fecha_hoy.month}/{fecha_hoy.day}.txt", datos_aemet)
```
```python
CSV playas leído.
AEMET: datos obtenidos.
Dataframe subido a s3://bronce-guille/bronce/catalogos/guia_playas/v1/playas.csv
Texto subido a s3://bronce-guille/bronce/meteorologia/prediccion_playas/2026/4/8.txt
```