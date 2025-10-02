asignaturas = {
    "Matemáticas": ["Ana", "Carlos", "Luis", "María", "Jorge"],
    "Física": ["Elena", "Luis", "Juan", "Sofía"],
    "Programación": ["Ana", "Carlos", "Sofía", "Jorge", "Pedro"],
    "Historia": ["María", "Juan", "Elena", "Ana"],
    "Inglés": ["Carlos", "Sofía", "Jorge", "María"],
}

while True:
    print("1.- Listar estudiantes de una asignatura")
    print("2.- Matricular estudiantes")
    print("3.- Dar de baja un estudiante")
    print("4.- Salir")
    op = input("Elige una opción: ")
    match op:
        case "1":
            #Listar estudiantes matriculados en una asignatura
            asig = input("Dime el nombre de la asignatura: ")
            print(asignaturas[asig]) #También print(asignaturas.get(asig))

        case "2":
            #Matricular estudiantes
            alumno = input("Dime el nombre de alumno: ")
            asig = input("Dime el nombre de la asignatura: ")
            if asig in asignaturas:
                asignaturas[asig].append(alumno)
            else:
                asignaturas[asig] = [alumno]

        case "3":
            #Dar de baja un estudiante
            alumno = input("Dime el alumno a dar de baja: ")
            asig = input("Dime la asignatura en la que darle de baja: ")
            asignaturas[asig].remove(alumno)

        case _:
            salir = True