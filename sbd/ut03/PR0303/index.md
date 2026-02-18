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

## 2.- Gestión de paginación
```python
all_people = []
url = "https://swapi.dev/api/people/"

while url:
    response = requests.get(url)
    data = response.json()
    all_people.extend(data['results'])
    url = data['next']

df = pd.DataFrame(all_people)

total_count = data['count']
print(f"Filas en DataFrame: {len(df)}")
print(f"Total según API: {total_count}")
print("Coincide:", len(df) == total_count)
```

## 3.- Cruce de datos
```python
def get_planet_info(planet_url):
    if not planet_url:
        return (None, None, None)
    response = requests.get(planet_url)
    data = response.json()
    return (data.get('name'), data.get('terrain'), data.get('population'))

planet_data = df.loc[:19, 'homeworld'].apply(get_planet_info)

planet_df = pd.DataFrame(planet_data.tolist(), columns=['planet_name', 'planet_terrain', 'planet_population'])

df_enriched = pd.concat([df.loc[:19].reset_index(drop=True), planet_df], axis=1)

print(df_enriched.head())
```

## 4.- Expansión de filas (opcional)
```python
df_subset = df_enriched.head(20).copy()

df_exploded = df_subset.explode('films').reset_index(drop=True)

def get_film_title(film_url):
    if not film_url:
        return None
    response = requests.get(film_url)
    data = response.json()
    return data.get('title')

df_exploded['films'] = df_exploded['films'].apply(get_film_title)

print(df_exploded[['name', 'films']].head(10))
```