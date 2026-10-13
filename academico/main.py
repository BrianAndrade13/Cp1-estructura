from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet (ej. EST2026001): "),
        "carrera": input("Carrera: "),
    }
    exito, mensaje = estudiantes.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún estudiante coincide con '{termino}'.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        pausa()
        return

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = estudiantes.actualizar(id_estudiante, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        pausa()
        return

    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, mensaje = estudiantes.eliminar(id_estudiante)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def mostrar_por_carrera():
    imprimir_titulo("ESTUDIANTES POR CARRERA")
    agrupados = estudiantes.estudiantes_por_carrera()
    if not agrupados:
        imprimir_info("Todavía no hay estudiantes.")
        pausa()
        return

    for carrera, nombres in agrupados.items():
        print(f"  {carrera:<20}: {', '.join(nombres)}")
    pausa()


def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código (ej. MAT101): "),
        "creditos": input("Créditos (1 a 10): "),
        "cupos": input("Cupos (0 a 30): "),
    }
    exito, mensaje = materias.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")
    encontradas = materias.buscar(termino)
    mostrar_lista(encontradas, f"Ninguna materia coincide con '{termino}'.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(materia)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrada")
        pausa()
        return

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = materias.actualizar(id_materia, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrada")
        pausa()
        return

    imprimir_info(f"Se eliminará: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, mensaje = materias.eliminar(id_materia)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def matricular():
    imprimir_titulo("MATRICULAR")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo (ej. 2026-1): "),
    }
    if None in datos.values():
        imprimir_error("Los ids deben ser números enteros")
        pausa()
        return

    exito, mensaje = matriculas.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")
    pausa()


def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")
    id_matricula = pedir_entero("Id de la matrícula: ")
    if id_matricula is None:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    nota = input("Nota (0 a 20): ")
    exito, mensaje = matriculas.registrar_nota(id_matricula, nota)
    mostrar_resultado(exito, mensaje)
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print(texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_matricula = pedir_entero("Id de la matrícula: ")
    if id_matricula is None:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    if confirmar("Se devolverá el cupo. ¿Confirma?"):
        exito, mensaje = matriculas.eliminar(id_matricula)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def ver_matriculas_por_estudiante():
    imprimir_titulo("MATRÍCULAS POR ESTUDIANTE")
    agrupadas = matriculas.matriculas_por_estudiante()
    if not agrupadas:
        imprimir_info("Todavía no hay matrículas.")
        pausa()
        return

    for id_estudiante, lista in agrupadas.items():
        estudiante = estudiantes.obtener(id_estudiante)
        if estudiante is None:
            print(f"  Estudiante {id_estudiante} (eliminado)")
        else:
            print(f"  {estudiante.etiqueta()}")
        for matricula in lista:
            print(f"      {matricula}")
    pausa()


def ver_promedio():
    imprimir_titulo("PROMEDIO DE UN ESTUDIANTE")
    id_estudiante = pedir_entero("Id del estudiante: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        pausa()
        return

    promedio = matriculas.promedio_de_estudiante(id_estudiante)
    print(f"  {estudiante.etiqueta()}")
    if promedio is None:
        imprimir_info("Todavía no tiene notas registradas.")
    else:
        print(f"  Promedio: {promedio}")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN")
    nombres_sin_cupo = []
    for materia in materias.materias_sin_cupo():
        nombres_sin_cupo.append(materia.nombre)

    print(f"  Estudiantes       : {len(estudiantes.leer())}")
    print(f"  Carreras          : {', '.join(estudiantes.carreras()) or '-'}")
    print(f"  Materias          : {len(materias.leer())}")
    print(f"  Materias sin cupo : {', '.join(nombres_sin_cupo) or 'ninguna'}")
    print(f"  Matrículas        : {len(matriculas.leer())}")
    print(f"  Aprobadas         : {matriculas.cantidad_aprobadas()}")
    pausa()


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla in opciones:
            print(f"  {tecla}. {opciones[tecla][0]}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        funcion = opciones[tecla][1]
        if funcion is None:
            break
        funcion()


def menu_estudiantes():
    ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)


def menu_materias():
    ejecutar_menu("MATERIAS", MENU_MATERIAS)


def menu_matriculas():
    ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)


MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "7": ("Estudiantes por carrera", mostrar_por_carrera),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Matricular", matricular),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "6": ("Matrículas por estudiante", ver_matriculas_por_estudiante),
    "7": ("Promedio de un estudiante", ver_promedio),
    "0": ("Volver", None),
}

MENU_PRINCIPAL = {
    "1": ("Estudiantes", menu_estudiantes),
    "2": ("Materias", menu_materias),
    "3": ("Matrículas", menu_matriculas),
    "4": ("Resumen", resumen),
    "0": ("Salir", None),
}


def main():
    ejecutar_menu("SISTEMA ACADÉMICO", MENU_PRINCIPAL)
    imprimir_info("¡Hasta luego!")


if __name__ == "__main__":
    main()
