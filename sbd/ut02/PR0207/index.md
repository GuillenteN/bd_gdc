# PR0206: Ingesta de datos financieros en InfluxDB

## Desarrollar el script `ingesta_crypto.py`
```python
import os
import csv
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions

DATA_DIR = "data/crypto_files/"
INFLUX_URL = "http://influxdb2:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="
INFLUX_ORG = "docs"
BUCKET = "crypto_raw"

puntos_insertados = 0

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=WriteOptions(write_type=ASYNCHRONOUS, batch_size=5000))

def procesar_fichero(filepath):
    global puntos_insertados
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name      = row[1]
            symbol    = row[2]
            date_str  = row[3]
            high      = float(row[4])
            low       = float(row[5])
            open_     = float(row[6])
            close     = float(row[7])
            volume    = float(row[8])
            marketcap = float(row[9])
            fecha = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            fecha_utc= fecha.replace(tzinfo=timezone.utc)
            time_date = fecha_utc.isoformat().replace('+00:00','Z')
            p = (
                Point("daily_quote")
                .tag("symbol", symbol)
                .tag("name", name)
                .time(fecha, WritePrecision.NS)
                .field("close", float(close))
                .field("high", float(high))
                .field("low", float(low))
                .field("open", float(open_))
                .field("volume", float(volume))
                .field("marketcap", float(marketcap))
            )
            write_api.write(bucket=BUCKET, record=p)
            puntos_insertados += 1
    print(f"Fichero {os.path.basename(filepath)} procesado.")

def main():
    for fichero in os.listdir(DATA_DIR):
        if fichero.endswith(".csv"):
            procesar_fichero(os.path.join(DATA_DIR, fichero))
    write_api.close()
    print(f"Ingesta finalizada. Total puntos insertados: {puntos_insertados}")

if __name__ == "__main__":
    main()
```

![alt text](./salida1.png)