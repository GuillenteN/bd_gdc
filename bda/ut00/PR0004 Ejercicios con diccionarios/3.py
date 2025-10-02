frase = input("Escribe una frase: ")

# Convertimos a minúsculas y separamos en palabras
palabras = frase.lower().split()

frecuencias = {}
for palabra in palabras:
    if palabra in frecuencias:
        frecuencias[palabra] += 1
    else:
        frecuencias[palabra] = 1

# Mostramos el resultado
print("Frecuencia de palabras:")
for palabra, conteo in frecuencias.items():
    print(f"'{palabra}': {conteo}")