# PR0204: Datos geoespaciales en Redis

## Gestión de jugadores

### 1. Carga de datos `load_locations.py`
```python
for poi in POIS:
    poi_id = poi["id"]
    name = poi["name"]
    lon = poi["lon"]
    lat = poi["lat"]

    r.geoadd("poi:locations", (lon, lat, poi_id))

    r.hset("poi:info", poi_id, name)

    print("Datos cargados")
```

### 2. Búsqueda por radio `find_by_radius.py`
```python
def find_by_radius(lat, lon, distance):

    results = r.geosearch(
        "poi:locations",
        longitude=lon,
        latitude=lat,
        radius=distance,
        unit="m"
    )

    pois = []
    for poi_id in results:
        name = r.hget("poi:info", poi_id)
        if name:
            pois.append((poi_id.decode(), name.decode()))

    print(f"Encontrados {len(pois)} POIs en {distance/1000} km:")
    for poi_id, name in pois:
        print(f" -> {name} ({poi_id})")


```

## 3. Búsqueda del “más cercano” `find_nearest.py`
```python
def find_nearest(lat, lon):

    result = r.geosearch(
        "poi:locations",
        longitude=lon,
        latitude=lat,
        radius=100000,
        unit="m",
        sort="ASC",
        count=1,
        withdist=True
    )

    if not result:
        print("No se encontró ningún POI.")
        return

    poi_id, distance_m = result[0]

    name = r.hget("poi:info", poi_id)
    if name:
        name = name.decode()

    distance_km = float(distance_m) / 1000

    print(f'El POI más cercano es "{name}", que está a {distance_km:.2f} km.')
```