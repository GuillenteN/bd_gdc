# PR0403: Análisis de logs con MapReduce

```bash
!hdfs dfs -mkdir /analisis_logs
!hdfs dfs -put logfiles.log /analisis_logs
!head -n 100 logfiles.log > test_logfiles.log
```

## 1. Estadísticas básicas
### Contador de Códigos de Estado HTTP
#### - Mapper:
```bash
%%writefile mapper_1.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()

    print(f"{words[8]}\t1")
```
#### - Reducer:
```bash
%%writefile reducer_1.py
#!/usr/bin/env python3
import sys

current_code = 0
current_count = 0
for line in sys.stdin:
    code, count = line.strip().split("\t")
    code = int(code)

    if code == current_code:
        current_count += 1
    else:
        if current_code:
            print(f"{current_code}: {current_count}")
        current_code = code
        current_count = 0

if current_code:
     print(f"{current_code}: {current_count}")
```

#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_1.py \
-file reducer_1.py \
-mapper mapper_1.py \
-reducer reducer_1.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida
```

### Tráfico Total por IP
#### - Mapper:
```bash
%%writefile mapper_11.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()

    print(f"{words[0]}\t{words[9]}")
```
#### - Reducer:
```bash
%%writefile reducer_11.py
#!/usr/bin/env python3
import sys

current_ip = None
current_byte_count = 0
for line in sys.stdin:
    ip, byte_count = line.strip().split("\t")
    try:
        byte_count = float(byte_count)
    except ValueError:
        byte_count = 0
    if current_ip == ip:
        current_byte_count += byte_count
    else:
        if current_ip:
            print(f"{current_ip}\t{current_byte_count}")
            
        current_ip = ip
        current_byte_count = byte_count


print(f"{current_ip}\t{current_byte_count}")
```

#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_11.py \
-file reducer_11.py \
-mapper mapper_11.py \
-reducer reducer_11.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/ip_bytes
```

## 2. Analisis de comportamiento
### URLs más populares
#### - Mapper:
```bash
%%writefile mapper_2.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()

    print(f"{words[5]}{words[6]}{words[7]}\t1")
```
#### - Reducer:
```bash
%%writefile reducer_2.py
#!/usr/bin/env python3
import sys

current_url = None
current_count = 0
for line in sys.stdin:
    url, count = line.strip().split("\t")
    if current_url == url:
        current_count += 1
    else:
        if current_url:
            print(f"{current_url}: {current_count}")
        
        current_url = url
        current_count = 0


print(f"{current_url}: {current_count}")
```
#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_2.py \
-file reducer_2.py \
-mapper mapper_2.py \
-reducer reducer_2.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/urls
```

### Distribución por Método HTTP
#### - Mapper:
```bash
%%writefile mapper_21.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()

    print(f"{words[5]}\t1")
```
#### - Reducer:
```bash
%%writefile reducer_21.py
#!/usr/bin/env python3
import sys

current_http = None
current_count = 0
for line in sys.stdin:
    http, count = line.strip().split("\t")
    if current_http == http:
        current_count += 1
    else:
        if current_http:
            print(f"{current_http}: {current_count}")
        
        current_http = http
        current_count = 0


print(f"{current_http}: {current_count}")
```
#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_21.py \
-file reducer_21.py \
-mapper mapper_21.py \
-reducer reducer_21.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/http
```

### Análisis de navegadores
#### - Mapper:
```bash
%%writefile mapper_22.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()
    try:
        browser, port = words[-2].split("/")
        print(f"{browser}\t1")
    except ValueError:
        continue
```
#### - Reducer:
```bash
%%writefile reducer_22.py
#!/usr/bin/env python3
import sys

current_browser = None
current_count = 0
for line in sys.stdin:
    browser, count = line.strip().split("\t")
    if current_browser == browser:
        current_count += 1
    else:
        if current_browser:
            print(f"{current_browser}: {current_count}")
        
        current_browser = browser
        current_count = 0


print(f"{current_browser}: {current_count}")
```
#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_22.py \
-file reducer_22.py \
-mapper mapper_22.py \
-reducer reducer_22.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/browser
```

## 3. Análisis temporal y de sesión
### Picos de tráfico por hora
#### - Mapper:
```bash
%%writefile mapper_3.py
#!/usr/bin/env python3
from datetime import datetime
import sys

for line in sys.stdin:
    words = line.strip().split()
    datetime_string = words[3][1:]
    date_time = datetime.strptime(datetime_string, "%d/%b/%Y:%H:%M:%S")
    print(f"{date_time.hour}\t1")
```
#### - Reducer:
```bash
%%writefile reducer_3.py
#!/usr/bin/env python3
import sys

current_hour = None
current_count = 0
for line in sys.stdin:
    hour, count = line.strip().split("\t")
    if current_hour == hour:
        current_count += 1
    else:
        if current_hour:
            print(f"{current_hour}: {current_count}")
        
        current_hour = hour
        current_count = 0


print(f"{current_hour}: {current_count}")
```
#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_3.py \
-file reducer_3.py \
-mapper mapper_3.py \
-reducer reducer_3.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/hour
```

### Tasa de error por endpoint
#### - Mapper:
```bash
%%writefile mapper_31.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()
    url, http_code = words[6], int(words[8])
    status = None
    if http_code >= 400:
        status = (0, 1)
    elif http_code < 400:
        status = (1, 0)
    print(f"({url}, {status})")
```
#### - Reducer:
```bash
%%writefile reducer_31.py
#!/usr/bin/env python3
import sys

current_url = None
total_success = 0
total_errors = 0
error_percent = 0
for line in sys.stdin:
    try:
        url, status_success, status_error = line.strip("(").split(",")
        status_success = int(status_success[2:])
        status_error = int(status_error[:-3])

        if current_url == url:
            if status_success == 1:
                total_success += 1
    
            if status_error == 1:
                total_errors += 1
        else:
            if current_url:
                error_percent = (total_errors / (total_errors + total_success)) * 100
                print(f"{current_url}: {error_percent}%")
            
            current_url = url
            total_success = 0
            total_errors = 0
            error_percent = 0
    except ValueError:
        print("Fallo", status_success, status_error)


print(f"{current_url}: {error_percent}%")
```
#### - Ejecución:
```bash
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_31.py \
-file reducer_31.py \
-mapper mapper_31.py \
-reducer reducer_31.py \
-input /analisis_logs/logfiles.log \
-output /analisis_logs/salida/error_percent
```