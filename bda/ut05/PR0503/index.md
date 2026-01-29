# PR0503: Limpieza de datos sobre dataset de cultivos

## Dataset 1: Datos para la predicción del rendimiento en cultivos
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
df_crop = ( spark.read
           .format("csv")
           .schema(schema_cropyield)
           .option("header", "true")
           .load("crop_yield_dataset.csv")
)
```
### 1.- Creación de un ID único
```bash
df_eng = ( df_crop.withColumn("Region", substring(col("Region"), -1, 1))
                  .withColumn("Region", lpad(col("Region"), 3, "X"))
                  .withColumn("Crop", upper(col("Crop")))
                  .withColumn("Crop_ID",
                             concat_ws(
                                 "_",
                                 monotonically_increasing_id(),
                                  concat_ws(
                                     "-",
                                     col("region"),
                                     col("Crop")
                             )))
         )
```
```bash
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------+
|  Crop|Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|     Crop_ID|
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------+
| MAIZE|   XXC|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| 0_XXC-MAIZE|
|BARLEY|   XXD|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|1_XXD-BARLEY|
|  RICE|   XXC|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  2_XXC-RICE|
| MAIZE|   XXD|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| 3_XXD-MAIZE|
| MAIZE|   XXD|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| 4_XXD-MAIZE|
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------+
```
o
```bash
df_eng = ( df_crop.withColumn("Region", substring(col("Region"), -1, 1))
                  .withColumn("Region", lpad(col("Region"), 3, "X"))
                  .withColumn("Crop", upper(col("Crop")))
                  .withColumn("Crop_ID",
                                 concat(
                                    lit("CODIGO_"),
                                    col("region"),
                                    lit("-"),
                                    col("Crop")
                             ))
         )
```
```bash
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+-----------------+
|  Crop|Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|          Crop_ID|
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+-----------------+
| MAIZE|   XXC|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| CODIGO_XXC-MAIZE|
|BARLEY|   XXD|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|CODIGO_XXD-BARLEY|
|  RICE|   XXC|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  CODIGO_XXC-RICE|
| MAIZE|   XXD|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| CODIGO_XXD-MAIZE|
| MAIZE|   XXD|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| CODIGO_XXD-MAIZE|
+------+------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+-----------------+
```
### 2.- Transformación matemática
```bash

```