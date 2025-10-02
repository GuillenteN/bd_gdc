productos = {
    "Electrónica": ["Smartphone", "Laptop", "Tablet", "Auriculares", "Smartwatch"],
    "Hogar": ["Aspiradora", "Microondas", "Lámpara", "Sofá", "Cafetera"],
    "Ropa": ["Camisa", "Pantalones", "Chaqueta", "Zapatos", "Bufanda"],
    "Deportes": ["Pelota de fútbol", "Raqueta de tenis", "Bicicleta", "Pesas", "Cuerda de saltar"],
    "Juguetes": ["Muñeca", "Bloques de construcción", "Peluche", "Rompecabezas", "Coche de juguete"],
}
# Número de categorías
num_categorias = len(productos)

# Número de productos por categoría y total
total_productos = 0
print(f"Número de categorías: {num_categorias}\n")
for categoria, items in productos.items():
    cantidad = len(items)
    total_productos += cantidad
    print(f"Categoría '{categoria}' tiene {cantidad} productos.")

print(f"\nNúmero total de productos: {total_productos}")