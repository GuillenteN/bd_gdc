# PR0301: Lectura de datos de archivos

## 1. Ingesta CSV
```python
df = pd.read_csv(
    'ventas_norte.csv',
    sep=';',
    encoding='utf-8',
)
```
## 2. Ingesta Excel
```python
!pip install openpyxl
```
```python
df_xlsx = pd.read_excel(
    'ventas_sur.xlsx',
    sheet_name=None
)
df_xlsx = pd.concat(df_xlsx.values(), ignore_index=True)
df_xlsx.head()
```
## 3. Ingesta JSON (Semi-estructurado)
```python
import json

with open('ventas_este.json') as f:
    data = json.load(f)

df_json = pd.json_normalize(data)
```
## 4. Transformación y Limpieza
```python
df_csv = df_csv.rename(columns={
    "ID_Transaccion": "id",
    "Fecha_Venta": "fecha",
    "Nom_Producto": "producto",
    "Cantidad_Vendida": "cantidad",
    "Precio_Unit": "precio_unitario"
})
df_csv["region"] = "Norte"
```
```python
df_xlsx = df_xlsx.rename(columns={
    "SalesID": "id",
    "Date": "fecha",
    "Item": "producto",
    "Qty": "cantidad",
    "UnitPrice": "precio_unitario"
})
df_xlsx["region"] = "Sur"
```
```python
df_json = df_json.rename(columns={
    "id_orden": "id",
    "timestamp": "fecha",
    "detalles_producto.nombre": "producto",
    "detalles_producto.specs.cantidad": "cantidad",
    "detalles_producto.specs.precio": "precio_unitario"
})
df_json["region"] = "Este"
```
## 5. Consolidación
```python
df_total = pd.concat(
    [df_csv, df_xlsx, df_json],
    ignore_index=True
)
```
## 6. Exportación Estandarizada
```python
df_total.to_csv("ventas_consolidadas.csv", sep=",", encoding="utf-", index=False)
```