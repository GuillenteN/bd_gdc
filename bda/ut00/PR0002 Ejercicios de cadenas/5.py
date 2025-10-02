texto = input("Introduce una cadena: ")

resultado = ""
for letra in texto:
    if letra not in resultado:
        resultado += letra

print("Cadena sin duplicados:", resultado)
