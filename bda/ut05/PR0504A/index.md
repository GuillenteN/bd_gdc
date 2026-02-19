# PR0504A. Limpieza de datos sobre dataset de lugares famosos

## Dataset 2: Lugares famosos del mundo

```bash
schema_worldfamousplaces = StructType([
    StructField("PlaceName", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Annual_Visitors_Millions", DoubleType(), True),
    StructField("Type", StringType(), True),
    StructField("UNESCO_World_Heritage", StringType(), True),
    StructField("Year_Built", StringType(), True),
    StructField("Entry_Fee_USD", IntegerType(), True),
    StructField("Best_Visit_Month", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Tourism_Revenue_Million_USD", IntegerType(), True),
    StructField("Average_Visit_Duration_Hours", DoubleType(), True),
    StructField("Famous_For", StringType(), True),
])
```
```bash
df_worldfamousplaces = ( spark.read
                   .format("csv")
                   .schema(schema_worldfamousplaces)
                   .option("header", "true")
                   .load("world_famous_places_2024.csv")
               )
```
### Ejercicio 1: Generación de códigos SKUs
```bash

```
### Ejercicio 2: Ajuste de precios y tiempos
```bash

```
### Ejercicio 3: Limpieza de texto
```bash

```
### Ejercicio 4: Gestión de fechas de campaña
```bash

```