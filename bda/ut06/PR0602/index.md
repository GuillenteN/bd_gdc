# PR0602: AWS Lambda

## Ejercicio 1
![alt text](./ej1.png)

## Ejercicio 2
![alt text](./ej2.png)

## Ejercicio 3
![alt text](./ej3.png)

## Ejercicio 4
![alt text](./ej4.png)

## Ejercicio 5
```python
from dotenv import load_dotenv
import boto3
import json
import os

load_dotenv()
session = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        aws_session_token=os.getenv("aws_session_token"),
        region_name='us-east-1'
    )
sqs = session.client('sqs')

queue_url = 'MiBuzon'

datos_archivo = {
        "prioridad": "ALTA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

mensaje_serializado = json.dumps(datos_archivo)

response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)
print("Respuesta prioridad alta:", response)


datos_archivo = {
        "prioridad": "BAJA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

mensaje_serializado = json.dumps(datos_archivo)

response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)

print("Respuesta prioridad baja:", response)
datos_archivo = {
        "prioridad": "MEDIA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

mensaje_serializado = json.dumps(datos_archivo)

response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)

print("Respuesta prioridad media:", response)
```

```python

```
## Ejercicio 6
![alt text](./ej6-1.png)
![alt text](./ej6-2.png)

## Ejercicio 7
![alt text](./ej7.png)

## Ejercicio 8
![alt text](./ej8-1.png)
![alt text](./ej8-2.png)