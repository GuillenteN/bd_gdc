# PR0201: Cadenas en Redis

## 1. Trabajo con Redis CLI
### 1. Creamos una clave con el nombre
```CLI
SET usuario:nombre guille
```
### 2. Creamos una clave con el apellido
```CLI
SET usuario:apellido diez
```
### 3. Recuperamos el valor con GET
```CLI
GET usuario:nombre
GET usuario:apellido
```
### 4. Almacenamos y recuperamos un correo
```CLI
SET usuario:email guille@correo.com
GET usuario:email
```
### 5. Cambiamos el valor de usuario:nombre para que aparezca en mayúsculas
```CLI
SET usuario:nombre GUILLE
```
### 6. Creamos la clave "contador:visitas" con valor 0
```CLI
SET contador:visitas 0
```
### 7. Incrementamos su valor en 1, 3 veces
```CLI
INCR contador:visitas
INCR contador:visitas
INCR contador:visitas
```
### 8. Decrementamos su valor en 1
```CLI
DECR contador:visitas
```
### 9. Guardamos en la clave mensaje el texto "Bienvenido a Redis"
```CLI
SET mensaje "Bienvenido a Redis"
```
### 10. Establecemos un tiempo de expiración de 60 segundos para la clave mensaje
```CLI
EXPIRE mensaje 60
```
### 11. Eliminamos la clave usuario:apellido
```CLI
DEL usuario:apellido
```
### 12. Eliminamos el resto de claves
```CLI
DEL usuario:nombre
DEL usuario:email
DEL contador:visitas
```

## 2. Trabajo con Python
[Documento Markdown](./PR0201.md)

[Cuaderno Jupyter](./PR0201.ipynb)