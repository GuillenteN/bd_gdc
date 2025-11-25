# PR0205: Escritura de datos en InfluxDB

## Primero importamos las librerias necesarias y nos conectamos con influx definiendo el write
```python
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb2:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None
try:
    # 1. Inicializar el cliente
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
    )

    write_options = WriteOptions(
        batch_size=500,
        flush_interval=1000,
        write_type=ASYNCHRONOUS
    )

    write_api = client.write_api(write_options=write_options)

    # 2. Verificar la conexión con el servidor
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}...")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión exitosa!")
        print(f"[INFO]  Versión del servidor: {health.version}")
    else:
        print(f"[ERROR] Conexión fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")

except (InfluxDBError, NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f"   Detalle: {e}")
```

## Definimos una función para obtener las metricas del sistema
```python
import psutil
import time

# Obtener estadísticas de uso
def obtener_metricas_sistema(host_id):
    # Uso de CPU (promedio de los últimos segundos)
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Uso de RAM
    mem = psutil.virtual_memory()
    ram_used_gb = round(mem.used / (1024**3), 2) # Conversión a GB
    ram_percent = mem.percent
    
    # Uso de disco (en el punto de montaje raíz)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    
    return {
        'host': host_id,
        'cpu_percent': cpu_usage,
        'ram_used_gb': ram_used_gb,
        'ram_percent': ram_percent,
        'disk_percent': disk_percent
    }
```

## Definimos la función con el bucle que enviará los datos a influx
```python
def bucle_lectura():
    while True:
        datos = obtener_metricas_sistema("servidor_A")
        p = (
            Point("rendimiento_servidor")
            .tag("host_id", datos["host"])
            .tag("entorno", "produccion")
            .field("cpu_percent", float(datos["cpu_percent"]))
            .field("ram_percent", float(datos["ram_percent"]))
            .field("disk_percent", float(datos["disk_percent"]))
        )
        write_api.write(bucket="agente_monitoreo", record=p)
        time.sleep(1)
        print("Leyendo datos")
```

## Ejecutamos el bucle añadiendo una opción para poder pararlo con la entrada del teclado (no funciona en jupyter)
```python
try:
    bucle_lectura()
except KeyboardInterrupt:
    print("Cerrando...")
```