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
df_eng.show(5)
```