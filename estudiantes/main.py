from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota, promedio_de,
    promedio_por_materia, materias_ofertadas, estudiantes_por_materia,
    estudiantes_en_comun, estadisticas
)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_id(texto="Id del estudiante: "):
    try:
        return int(input(texto))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<14}{'NOMBRE':<25}{'EMAIL':<28}{'PROM.':<8}{'MATERIAS':<10}")
    print("-" * 90)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.carnet:<14}"
              f"{estudiante.obtener_nombre_completo():<25}{estudiante.email:<28}"
              f"{estudiante.obtener_promedio():<8}{len(estudiante.materias):<10}")
    print("-" * 90)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")

    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        pausa()
        return

    for clave, valor in estudiante.a_diccionario().items():
        print(f"  {clave.capitalize():<12}: {valor}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        pausa()
        return

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        pausa()
        return

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------- AGREGAR NOTA ----------
def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")

    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return

    materia = input("Materia: ")
    nota = input("Nota (0 a 20): ")

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    mostrar_resultado(exito, mensaje)
    pausa()


# ---------- VER PROMEDIO ----------
def opcion_ver_promedio():
    imprimir_titulo("PROMEDIO DEL ESTUDIANTE")

    id_estudiante = pedir_id()
    if id_estudiante is None:
        pausa()
        return

    exito, promedio = promedio_de(id_estudiante)
    if not exito:
        imprimir_error(promedio)
        pausa()
        return

    exito, por_materia = promedio_por_materia(id_estudiante)
    if not por_materia:
        imprimir_info("Este estudiante todavía no tiene notas registradas.")
        pausa()
        return

    for materia, valor in por_materia.items():
        print(f"  {materia:<20}: {valor}")
    print()
    imprimir_info(f"Promedio general: {promedio}")
    pausa()


# ---------- MATERIAS EN COMÚN ----------
def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")

    id_a = pedir_id("Id del primer estudiante: ")
    if id_a is None:
        pausa()
        return

    id_b = pedir_id("Id del segundo estudiante: ")
    if id_b is None:
        pausa()
        return

    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
        pausa()
        return

    if not resultado:
        imprimir_info("Esos dos estudiantes no comparten ninguna materia.")
    else:
        for materia in sorted(resultado):
            print(f"  - {materia}")
        print()
        imprimir_info(f"Comparten {len(resultado)} materia(s)")
    pausa()


# ---------- MATERIAS OFERTADAS ----------
def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")

    materias = materias_ofertadas()
    if not materias:
        imprimir_info("Todavía no hay materias registradas.")
    else:
        for materia in sorted(materias):
            print(f"  - {materia}")
        print()
        imprimir_info(f"Total: {len(materias)} materia(s) distintas")
    pausa()


# ---------- ESTUDIANTES POR MATERIA ----------
def opcion_estudiantes_por_materia():
    imprimir_titulo("ESTUDIANTES POR MATERIA")

    agrupados = estudiantes_por_materia()
    if not agrupados:
        imprimir_info("Todavía no hay materias con estudiantes.")
        pausa()
        return

    for materia, nombres in agrupados.items():
        print(f"  {materia:<20}: {', '.join(nombres)}")
    pausa()


# ---------- ESTADÍSTICAS ----------
def opcion_estadisticas():
    imprimir_titulo("ESTADÍSTICAS")

    datos = estadisticas()
    print(f"  Estudiantes registrados : {datos['total']}")
    print(f"  Materias distintas      : {len(datos['materias'])} -> {', '.join(datos['materias'])}")
    print(f"  Dominios de email       : {', '.join(datos['dominios'])}")
    print(f"  Sin notas               : {len(datos['sin_notas'])}")
    pausa()


def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias ofertadas", opcion_materias_ofertadas),
    "11": ("Estudiantes por materia", opcion_estudiantes_por_materia),
    "12": ("Estadísticas", opcion_estadisticas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla in OPCIONES:
        texto = OPCIONES[tecla][0]
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        funcion = OPCIONES[tecla][1]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    main()
