n = 0
while n % 2 == 0 or n <= 0:   # Mientras sea par o negativo...
    n = int(input("Introduce un número impar positivo: "))

for i in range(1, n + 1, 2):
    espacios = (n - i) // 2
    print(" " * espacios + "*" * i)
