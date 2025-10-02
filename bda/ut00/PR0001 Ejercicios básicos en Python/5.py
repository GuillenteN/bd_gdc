numeros = []

for i in range(5):
    num = float(input(f"Introduce el número {i+1}: "))
    numeros.append(num)

mayor = max(numeros)
menor = min(numeros)

print(f"El número mayor es {mayor} y el menor es {menor}")
