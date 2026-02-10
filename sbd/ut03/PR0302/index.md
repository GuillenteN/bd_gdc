# PR0302: Lectura avanzada de datos de archivos

## 1. Norte CSV
```python
df_csv = pd.read_csv(
    'ventas_norte_v2.csv',
    sep=';',
    encoding='utf-8',
)

df_csv["Total_Factura"] = (
    df_csv["Total_Factura"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
)
```
## 2. Sur XLSX
```python
df_xlsx = pd.read_excel(
    'ventas_sur_v2.xlsx',
    sheet_name=None
)
df_xlsx = pd.concat(df_xlsx.values(), ignore_index=True)
df_xlsx['Estado_Envio'] = df_xlsx['Estado_Envio'].astype('category')
```
## 3. Este JSON
```python
import json

with open('ventas_este_v2.json') as f:
    data = json.load(f)

df_json = pd.json_normalize(data)
cols_utiles = [
    'data.id_registro',
    'data.payload.fecha_evento',
    'data.payload.comprador.ubicacion.ciudad',
    'data.payload.transaccion.detalles_producto.nombre_comercial',
    'data.payload.transaccion.cantidad_comprada',
    'data.payload.transaccion.detalles_producto.precio_lista',
    'data.payload.transaccion.detalles_producto.impuestos.monto_iva'
]

df_json = df_json[cols_utiles]
df_json = df_json.rename(columns={
    'data.id_registro': 'id_registro',
    'data.payload.fecha_evento': 'fecha',
    'data.payload.comprador.ubicacion.ciudad': 'ciudad',
    'data.payload.transaccion.detalles_producto.nombre_comercial': 'producto',
    'data.payload.transaccion.cantidad_comprada': 'cantidad',
    'data.payload.transaccion.detalles_producto.precio_lista': 'precio_lista',
    'data.payload.transaccion.detalles_producto.impuestos.monto_iva': 'monto_iva'
})
```

## Dataframe final
### CSV
```python
df_csv = ( df_csv
          .rename(columns={
            'ID_Pedido': 'id_transaccion',
            'Fecha_Transaccion': 'fecha',
            'Producto': 'producto',
            'Unidades': 'cantidad',
            'Total_Factura': 'total_venta',
            'Direccion_Envio': 'ciudad'
          })
)
df_csv = df_csv[['id_transaccion', 'fecha', 'producto', 'cantidad', 'total_venta', 'ciudad']]
```
### XLSX
```python
df_xlsx = ( df_xlsx
          .rename(columns={
            'Ref_Venta': 'id_transaccion',
            'Fecha_Alta': 'fecha',
            'Articulo': 'producto',
            'Cantidad': 'cantidad',
            'Precio_Base': 'total_venta',
          })
)
df_xlsx = df_xlsx[['id_transaccion', 'fecha', 'producto', 'cantidad', 'total_venta']]
```
### JSON
```python
df_json = ( df_json
          .rename(columns={
            'id_registro': 'id_transaccion',
            'fecha': 'fecha',
            'producto': 'producto',
            'cantidad': 'cantidad',
            'precio_lista': 'total_venta',
            'ciudad': 'ciudad'
          })
)
df_json = df_json[['id_transaccion', 'fecha', 'producto', 'cantidad', 'total_venta', 'ciudad']]
```
### FINAL
```python
df_final = pd.concat([df_csv, df_xlsx, df_json])
df_final.head()
```