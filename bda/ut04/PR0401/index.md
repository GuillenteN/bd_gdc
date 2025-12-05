# PR0401: Contando palabras
## 1. Contando palabras
Mapper:
```bash
%%writefile mapper_1.py
#!/usr/bin/env python3

import sys

palabras_normalizar = "\"!·$%&/()=?¿^*¨_:;,.-´`+¡'ºª\|@#~€¬{[]}\¸~ ̣·•• ´´“1234567890\t\n\r\a\b\f\r\t\v\\\n\r–‘‘«»"

for line in sys.stdin:
    words = line.split()
    for word in words:
        token = "".join(filter(lambda c: c not in palabras_normalizar, word.lower()))
        if token:
            print(f"{token}\t1")
```
Reducer:
```bash
%%writefile reducer_1.py
#!/usr/bin/env python3

import sys

current_word = None
count = 0

for line in sys.stdin:
    word, _ = line.split("\t")

    if current_word == word:
        count += 1
    else:
        if current_word:
            print(f"{current_word},{count}")
        current_word = word
        count = 1

if current_word:
    print(f"{current_word},{count}")
```

## 2. Filtrado de palabras representativas
Mapper:
```bash
%%writefile mapper_2.py
#!/usr/bin/env python3

import sys
import re

palabras_repre = ["a", "con", "de", "desde", "en", "hacia", "hasta", "mediante" \
                  "para", "por", "según", "sin", "so", "sobre", "tras", "versus", "vía", "de", "la", "el", "y", "en", "que", "los", "del", "se"]

for line in sys.stdin:
    words = line.strip().split()

    for word in words:
        word = re.sub(r'[^\w]', '', word).lower()
        
        if word and word not in palabras_repre:
            print(f"{word}\t1")
```

## 3. Ordenación por Frecuencia (Top-N)
Mapper :
```bash
%%writefile mapper_3.py
#!/usr/bin/env python3

import sys
import re

digitos = 5
for line in sys.stdin:
    word, count = line.strip().split("\t")
    length_count = len(count)

    new_count = ""
    if length_count < digitos:

        for i in range(digitos - length_count):
            new_count += "0"

        new_count += count
        print(f"{new_count}\t{word}")
```