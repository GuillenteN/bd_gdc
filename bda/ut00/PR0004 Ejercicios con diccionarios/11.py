#Escribe un programa que tome una cadena y use un diccionario para contar cuantas veces aparece cada caracter

str = "Especialización en Inteligencia Artificial y Big Data"
res = {}
for char in str.lower():
    if char in res:
        res[char] += 1
    else:
        res[char] = 1
print(res)