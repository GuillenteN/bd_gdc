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