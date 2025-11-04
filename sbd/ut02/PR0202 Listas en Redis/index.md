# PR0202: Listas en Redis

## 1. Importamos las librerias necesarias y nos conectamos con la base de datos
```python
import redis
import json
r = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)
r.ping()
```

## 2. Definimos la función que agregará los pedidos
```python
def agregar_pedido(cliente, producto):
    pedido_id = f"pedido_{r.llen('pedidos') + 1:03d}"
    pedido = {
        "id": pedido_id,
        "cliente": cliente,
        "producto": producto,
        "cantidad": 1,
        "urgente": False
    }
    pedido_json = json.dumps(pedido, ensure_ascii=False)
    r.rpush("pedidos", pedido_json)
    print("Pedido agregado correctamente")
```

## 3. Definimos la función que procesará los pedidos
```python
def procesar_pedido():
    pedido_json = r.lpop("pedidos")
    pedido = json.loads(pedido_json)
    print(f"Procesando pedido: {pedido['id']}")
```

## 5. Insertamos 5 pedidos iniciales
```python
agregar_pedido("Juan Pérez", "Portátil Lenovo")
agregar_pedido("Laura Cid", "Ratón HP")
agregar_pedido("Manolo Fernández", "Teclado Logitech")
agregar_pedido("María Rodríguez", "Portátil MSI")
agregar_pedido("Luis Díez", "Portátil Lenovo")
```
![alt text](./salida1.png)

## 6. Mostramos todos los pedidos en cola
```python
pedidos_json = r.lrange("pedidos", 0, -1)
print(f"Pedidos actuales en la cola ({len(pedidos_json)}):")
for i, p in enumerate(pedidos_json, start=1):
    pedido = json.loads(p)
    print(f"--- Pedido {i} ---")
    print(f"ID: {pedido['id']}")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Producto: {pedido['producto']}")
    print(f"Cantidad: {pedido['cantidad']}")
    print(f"Urgente: {'Sí' if pedido['urgente'] else 'No'}\n")
```
![alt text](./salida2.png)

## 7. Insertamos 2 pedidos más
```python
agregar_pedido("Marcos Serrano", "Portátil Lenovo")
agregar_pedido("Irene González", "Ratón HP")
```
![alt text](./salida3.png)

## 8. Procesamos todos los pedidos hasta que no queden
```python
while r.llen("pedidos") > 0:
        procesar_pedido()
```
![alt text](./salida4.png)

## 9. Agregamos un pedido urgente
```Python
def agregar_pedido_urgente(cliente, producto):
    pedido_id = f"pedido_{r.llen('pedidos') + 1:03d}"
    pedido = {
        "id": pedido_id,
        "cliente": cliente,
        "producto": producto,
        "cantidad": 1,
        "urgente": True
    }
    pedido_json = json.dumps(pedido, ensure_ascii=False)
    r.lpush("pedidos", pedido_json)
    print("Pedido agregado correctamente")

agregar_pedido("Pedro", "Ratón HP", True)
```
![alt text](./salida5.png)

## 10. Procesamos el pedido urgente antes que el resto
Al añadir el pedido con lpush se añade al principio, por lo que como los urgentes se añaden al principio se procesan los primeros.
```Python
procesar_pedido()
```
