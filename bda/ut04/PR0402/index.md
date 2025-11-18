# PR0402: Datos del clima
## 1. Temperatura máxima por ciudad
### Mapper:
```bash
%%writefile mapper_2.py
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
%%writefile reducer_2.py
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