# PR0303: Obtención de datos de una API REST

## 1.- Conexión básica y primer dataFrame
### 1
```python
!pip install requests
import requests

url = 'https://swapi.dev/api/vehicles/'

response = requests.get(url)

if response.status_code == 200:
    print("Éxito, conexión establecida")
    datos = response.json()
    print(datos)

else:
    print(f"Error: {response.status_code}")
```
### 2
```python
results = datos["results"]
print(results)
```
### 3
```python
import pandas as pd

df = pd.json_normalize(results)
```
### 4
```python
df.head(5)
df.columns
```