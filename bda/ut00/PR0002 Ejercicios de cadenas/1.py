texto = input("Introduce un texto: ")

vocales = "aeiouAEIOUáéíóúÁÉÍÓÚüÜ"
contador_vocales = 0
contador_consonantes = 0

for letra in texto:
    if letra.isalpha():
        if letra in vocales:
            contador_vocales += 1
        else:
            contador_consonantes += 1

print(f"Vocales: {contador_vocales}, Consonantes: {contador_consonantes}")
