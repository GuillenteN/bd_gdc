texto = input("Introduce una cadena: ")

texto_invertido = texto[::-1]

if texto == texto_invertido:
    print("Es un palíndromo")
else:
    print("No es un palíndromo")
