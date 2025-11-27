# PR0402: Datos del clima
## 1. Temperatura máxima por ciudad
### Mapper:
```bash
%%writefile mapper_1.py
#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
next(reader, None)

for row in reader:
    print(f"{row[3]}\t{row[7]}")
```
### Reducer:
```bash
%%writefile reducer_1.py
#!/usr/bin/env python3
import sys

current_city = None
max_temp = float('-inf')

for line in sys.stdin:
    line = line.strip()
    city, temp = line.split("\t")
    temp = float(temp)
    
    if current_city is not None and city != current_city:
        print(f"{current_city}\t{max_temp}")
        max_temp = float('-inf')

    current_city = city
    max_temp = max(max_temp, temp)

if current_city is not None:
    print(f"{current_city}\t{max_temp}")
```
### Lanzamos el proceso:
```bash
!hdfs dfs -put city_temperature.csv /
```
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_2.py \
-file reducer_2.py\
-mapper mapper_2.py\
-reducer reducer_2.py \
-input /city_temperature.csv \
-output /salida_PR0402
```

## 2. Media histórica por país
### Reducer
```python
%%writefile reducer_2.py
#!/usr/bin/env python3
import sys

current_country = None
temp_sum = 0.0
temp_count = 0

for line in sys.stdin:
    line = line.strip()
    country, temp = line.split("\t")
    temp = float(temp)

    if current_country is not None and country != current_country:
        avg_temp = temp_sum / temp_count
        print(f"{current_country}\t{avg_temp}")
        
        temp_sum = 0.0
        temp_count = 0

    current_country = country
    temp_sum += temp
    temp_count += 1

if current_country is not None:
    avg_temp = temp_sum / temp_count
    print(f"{current_country}\t{avg_temp}")
```

## 3. Conteo de días calurosos por ciudad
### Mapper
```python
%%writefile mapper_3.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split(",")
    if len(parts) < 3:
        continue

    city, date, temp = parts[:3]
    try:
        year = date.split("-")[0]
        temp = float(temp)
        print(f"{city}\t{year}\t{temp}")
    except ValueError:
        continue
```
### Reducer
```python
%%writefile reducer_3.py
#!/usr/bin/env python3
import sys

current_key = None
hot_days = 0

for line in sys.stdin:
    line = line.strip()
    city, year, temp = line.split("\t")
    temp = float(temp)
    key = f"{city}\t{year}"

    if current_key is not None and key != current_key:
        print(f"{current_key}\t{hot_days}")
        hot_days = 0

    current_key = key
    if temp > 30:
        hot_days += 1

if current_key is not None:
    print(f"{current_key}\t{hot_days}")
```

## 4.Rango de temperaturas por ciudad (Min/Max)
### Mapper
```python
%%writefile mapper_4.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split(",")
    if len(parts) < 3:
        continue

    city, date, temp = parts[:3]
    try:
        temp = float(temp)
        print(f"{city}\t{temp}")
    except ValueError:
        continue
```
## Reducer
```python
%%writefile reducer_4.py
#!/usr/bin/env python3
import sys

current_city = None
min_temp = float('inf')
max_temp = float('-inf')

for line in sys.stdin:
    line = line.strip()
    city, temp = line.split("\t")
    temp = float(temp)

    if current_city is not None and city != current_city:
        print(f"{current_city}\t{min_temp}\t{max_temp}")
        min_temp = float('inf')
        max_temp = float('-inf')

    current_city = city
    min_temp = min(min_temp, temp)
    max_temp = max(max_temp, temp)

if current_city is not None:
    print(f"{current_city}\t{min_temp}\t{max_temp}")
```