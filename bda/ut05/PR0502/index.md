# PR0502: Manipulación básica de dataframes

## Dataset 1: Datos para la predicción del rendimiento en cultivos
### 1.- Selección de características
```bash
schema_cropyield = StructType([
    StructField("Crop", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Soil_Type", StringType(), True),
    StructField("Soil_pH", DoubleType(), True),
    StructField("Rainfall_mm", DoubleType(), True),
    StructField("Temperature_C", DoubleType(), True),
    StructField("Humidity_pct", DoubleType(), True),
    StructField("Fertilizer_Used_kg", DoubleType(), True),
    StructField("Irrigation", StringType(), True),
    StructField("Pesticides_Used_kg", DoubleType(), True),
    StructField("Planting_Density", DoubleType(), True),
    StructField("Previous_Crop", StringType(), True),
    StructField("Yield_ton_per_ha", DoubleType(), True),
])
```
```bash
df_sel = ( spark.read
           .format("csv")
           .schema(schema_cropyield)
           .option("header", "true")
           .load("crop_yield_dataset.csv")
           .select("Crop", "Region", "Temperature_C", "Rainfall_mm", "Irrigation", "Yield_ton_per_ha")
)
```
o
```bash
df_sel = (df_crop
            .select("Crop", "Region", "Temperature_C", "Rainfall_mm", "Irrigation", "Yield_ton_per_ha")
)
```
```bash
+------+--------+-------------+-----------+----------+----------------+
|  Crop|  Region|Temperature_C|Rainfall_mm|Irrigation|Yield_ton_per_ha|
+------+--------+-------------+-----------+----------+----------------+
| Maize|Region_C|         19.7|     1485.4|      Drip|          101.48|
|Barley|Region_D|         29.1|      399.4| Sprinkler|          127.39|
|  Rice|Region_C|         30.5|      980.9| Sprinkler|           68.99|
| Maize|Region_D|         26.4|     1054.3|      Drip|          169.06|
| Maize|Region_D|         20.4|      744.6|      Drip|          118.71|
+------+--------+-------------+-----------+----------+----------------+
```

### 2.- Normalización de nombres
```bash
df_renamed = (df_sel
     .withColumnRenamed("Temperature_C", "Temperatura")
     .withColumnRenamed("Rainfall_mm", "Lluvia")
     .withColumnRenamed("Yield_ton_per_ha", "Rendimiento")
)

df_renamed.show(5)
```
```bash
+------+--------+-----------+------+----------+-----------+
|  Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
+------+--------+-----------+------+----------+-----------+
| Maize|Region_C|       19.7|1485.4|      Drip|     101.48|
|Barley|Region_D|       29.1| 399.4| Sprinkler|     127.39|
|  Rice|Region_C|       30.5| 980.9| Sprinkler|      68.99|
| Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
| Maize|Region_D|       20.4| 744.6|      Drip|     118.71|
+------+--------+-----------+------+----------+-----------+
```

### 3.- Filtrado de datos (filter)
```bash
df_renamed_filter = (df_renamed
     .filter(
         (col("Crop") == "Maize") & (col("Temperatura") > 25)
     )
)
df_renamed_filter.show()
```
```bash
+-----+--------+-----------+------+----------+-----------+
| Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
+-----+--------+-----------+------+----------+-----------+
|Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
|Maize|Region_C|       32.4| 846.1|      None|      162.2|
|Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
|Maize|Region_C|       33.7|1193.3|      None|     110.57|
|Maize|Region_C|       27.8| 695.2|     Flood|     143.84|
|Maize|Region_D|       30.2|1001.4|     Flood|     138.61|
|Maize|Region_A|       27.7| 747.7| Sprinkler|     114.58|
|Maize|Region_B|       28.9|1392.9|      Drip|     169.23|
|Maize|Region_B|       34.7| 694.4|      Drip|      96.08|
|Maize|Region_D|       29.5| 848.8|     Flood|      93.45|
|Maize|Region_D|       32.8|1067.7|     Flood|      154.6|
|Maize|Region_A|       28.5| 406.1| Sprinkler|      55.26|
|Maize|Region_D|       26.0| 391.4| Sprinkler|     100.34|
|Maize|Region_C|       25.9|1444.8| Sprinkler|      135.8|
|Maize|Region_D|       27.8| 823.3| Sprinkler|     161.48|
|Maize|Region_D|       28.7| 955.8|     Flood|       91.4|
|Maize|Region_A|       33.2| 248.4|      None|     149.49|
|Maize|Region_B|       34.3| 410.4|     Flood|      37.78|
|Maize|Region_A|       27.1| 763.9|      Drip|     110.63|
|Maize|Region_C|       28.8|1215.0|     Flood|     127.89|
+-----+--------+-----------+------+----------+-----------+
```

### 4.- Encadenamiento
```bash
df = (df_crop
        .select("Crop", "Region", "Temperature_C", "Rainfall_mm", "Irrigation", "Yield_ton_per_ha")
        .withColumnRenamed("Temperature_C", "Temperatura")
        .withColumnRenamed("Rainfall_mm", "Lluvia")
        .withColumnRenamed("Yield_ton_per_ha", "Rendimiento")
        .filter(
         (col("Crop") == "Maize") & (col("Temperatura") > 25)
     )
)
df.show()
```
```bash
+-----+--------+-----------+------+----------+-----------+
| Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
+-----+--------+-----------+------+----------+-----------+
|Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
|Maize|Region_C|       32.4| 846.1|      None|      162.2|
|Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
|Maize|Region_C|       33.7|1193.3|      None|     110.57|
|Maize|Region_C|       27.8| 695.2|     Flood|     143.84|
+-----+--------+-----------+------+----------+-----------+
```

## Dataset 2: Lugares famosos del mundo
### 1.- Selección de datos críticos
```bash
df_base = (df_worldfamous
            .select("Place_Name", "Country", "UNESCO_World_Heritage", "Entry_Fee_USD", "Annual_Visitors_Millions")
)
```
```bash
+-------------------+-------------+---------------------+-------------+------------------------+
|         Place_Name|      Country|UNESCO_World_Heritage|Entry_Fee_USD|Annual_Visitors_Millions|
+-------------------+-------------+---------------------+-------------+------------------------+
|       Eiffel Tower|       France|                   No|           35|                     7.0|
|       Times Square|United States|                   No|            0|                    50.0|
|      Louvre Museum|       France|                  Yes|           22|                     8.7|
|Great Wall of China|        China|                  Yes|           10|                    10.0|
|          Taj Mahal|        India|                  Yes|           15|                     7.5|
+-------------------+-------------+---------------------+-------------+------------------------+
```
### 2.- Traducción y simplificación
```bash
df_es = (df_base
            .withColumnRenamed("Place_Name", "Lugar")
            .withColumnRenamed("UNESCO_World_Heritage", "Es_UNESCO")
            .withColumnRenamed("Entry_Fee_USD", "Precio_Entrada")
            .withColumnRenamed("Annual_Visitors_Millions", "Visitantes_Millones")
)
```
```bash
+-------------------+-------------+---------+--------------+-------------------+
|              Lugar|      Country|Es_UNESCO|Precio_Entrada|Visitantes_Millones|
+-------------------+-------------+---------+--------------+-------------------+
|       Eiffel Tower|       France|       No|            35|                7.0|
|       Times Square|United States|       No|             0|               50.0|
|      Louvre Museum|       France|      Yes|            22|                8.7|
|Great Wall of China|        China|      Yes|            10|               10.0|
|          Taj Mahal|        India|      Yes|            15|                7.5|
+-------------------+-------------+---------+--------------+-------------------+
```
### 3.- Filtrado
```bash
df_es = (df_es
            .filter(
                (col("Es_UNESCO") == "Yes") & (col("Precio_Entrada") <= 20)
            )
)
```
```bash
+--------------------+--------------+---------+--------------+-------------------+
|               Lugar|       Country|Es_UNESCO|Precio_Entrada|Visitantes_Millones|
+--------------------+--------------+---------+--------------+-------------------+
| Great Wall of China|         China|      Yes|            10|               10.0|
|           Taj Mahal|         India|      Yes|            15|                7.5|
|           Colosseum|         Italy|      Yes|            18|               7.65|
|      Forbidden City|         China|      Yes|             8|                9.0|
|Notre-Dame Cathedral|        France|      Yes|             0|               13.0|
|Great Pyramid of ...|         Egypt|      Yes|            20|                2.8|
|Leaning Tower of ...|         Italy|      Yes|            20|                5.0|
|           Acropolis|        Greece|      Yes|            13|                4.0|
|             Big Ben|United Kingdom|      Yes|             0|                5.5|
+--------------------+--------------+---------+--------------+-------------------+
```

## Dataset 3: Registro turístico de Castilla y León
### 1.- Selección y saneamiento
```bash
df_contactos = (df_turismo
                    .select("Nombre", "Tipo", "Provincia", "web", "Email")
)
```
```bash
+--------------------+--------------------+---------+--------------------+--------------------+
|              Nombre|                Tipo|Provincia|                 web|               Email|
+--------------------+--------------------+---------+--------------------+--------------------+
|BERNARDO MORO MEN...|Profesional de Tu...| Asturias|                NULL|bernardomoro@hotm...|
|        LA SASTRERÍA|Casa Rural de Alq...|    Ávila|www.lasastreriade...|                NULL|
|         LAS HAZANAS|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
| LA CASITA DEL PAJAR|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
|            MARACANA|                 Bar|    Ávila|                NULL|emo123anatoliev@g...|
+--------------------+--------------------+---------+--------------------+--------------------+
```
### 2.- Renombrado estándar
```bash
df_limpio = (df_contactos
                .withColumnRenamed("Nombre", "nombre_establecimiento")
                .withColumnRenamed("Tipo", "categoria_actividad")
                .withColumnRenamed("web", "sitio_web")
                .withColumnRenamed("Email", "correo_electronico")
)
```
```bash
+----------------------+--------------------+---------+--------------------+--------------------+
|nombre_establecimiento| categoria_actividad|Provincia|           sitio_web|  correo_electronico|
+----------------------+--------------------+---------+--------------------+--------------------+
|  BERNARDO MORO MEN...|Profesional de Tu...| Asturias|                NULL|bernardomoro@hotm...|
|          LA SASTRERÍA|Casa Rural de Alq...|    Ávila|www.lasastreriade...|                NULL|
|           LAS HAZANAS|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
|   LA CASITA DEL PAJAR|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
|              MARACANA|                 Bar|    Ávila|                NULL|emo123anatoliev@g...|
+----------------------+--------------------+---------+--------------------+--------------------+
```
### 3: Filtrado de texto
```bash
df_final = (df_limpio
                .filter(
                    (col("Provincia") == "Burgos") &
                    (col("categoria_actividad").like("%Bodega%")) &
                    (col("sitio_web").isNotNull())
                )
)
```
```bash
+----------------------+--------------------+---------+--------------------+--------------------+
|nombre_establecimiento| categoria_actividad|Provincia|           sitio_web|  correo_electronico|
+----------------------+--------------------+---------+--------------------+--------------------+
|        BODEGAS TARSUS|g - Bodegas y los...|   Burgos|  www.tarsusvino.com|                NULL|
|  BODEGAS DOMINIO D...|g - Bodegas y los...|   Burgos|www.dominiodecair...|bodegas@dominiode...|
|    TERRITORIO LUTHIER|g - Bodegas y los...|   Burgos|territorioluthier...|luthier@territori...|
|    BODEGA COVARRUBIAS|g - Bodegas y los...|   Burgos| http://valdable.com|   info@valdable.com|
|  BODEGAS PASCUAL, ...|g - Bodegas y los...|   Burgos|222.bodegaspascua...|export@bodegaspas...|
+----------------------+--------------------+---------+--------------------+--------------------+
```