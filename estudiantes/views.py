import os

from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

CARPETA = os.path.dirname(os.path.abspath(__file__))
gestor = GestorJSON(os.path.join(CARPETA, "data", "estudiantes.json"))

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

NOTA_MINIMA = 0
NOTA_MAXIMA = 20


# ===================== AYUDAS =====================

def emails_registrados(excepto_id=None):
    emails = set()
    for registro in gestor.leer():
        if registro["id"] != excepto_id:
            emails.add(registro["email"].lower())
    return emails


def carnets_registrados(excepto_id=None):
    carnets = set()
    for registro in gestor.leer():
        if registro["id"] != excepto_id:
            carnets.add(registro["carnet"].upper())
    return carnets


def siguiente_id():
    ids = []
    for registro in gestor.leer():
        ids.append(registro["id"])

    if not ids:
        return 1
    return max(ids) + 1


def buscar_posicion(registros, id_estudiante):
    for posicion, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            return posicion
    return None


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    valores = {}
    for campo in CAMPOS_ESTUDIANTE:
        valores[campo] = str(datos.get(campo, "")).strip()
    valores["carnet"] = valores["carnet"].upper()

    for campo in CAMPOS_OBLIGATORIOS:
        if not valores[campo]:
            return False, f"Falta el campo {campo}"

    if not es_email_valido(valores["email"]):
        return False, f"El email '{valores['email']}' no tiene un formato válido"

    if valores["email"].lower() in emails_registrados():
        return False, "Ese email ya está registrado"

    if valores["carnet"] in carnets_registrados():
        return False, f"El carnet {valores['carnet']} ya está registrado"

    estudiante = Estudiante(
        siguiente_id(),
        valores["nombre"],
        valores["apellido"],
        valores["email"],
        valores["carnet"],
    )

    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"

    return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"


# ===================== R · READ =====================

def obtener_todos():
    estudiantes = []  # lista porque los registros se recorren en orden y crecen
    for registro in gestor.leer():
        estudiantes.append(Estudiante.desde_diccionario(registro))
    return estudiantes


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    if not cambios:
        return False, "No se indicó ningún cambio"

    desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

    if "email" in cambios:
        if not es_email_valido(cambios["email"]):
            return False, "El email no tiene un formato válido"
        if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
            return False, "Ese email ya lo usa otro estudiante"

    if "carnet" in cambios:
        cambios["carnet"] = cambios["carnet"].strip().upper()
        if not cambios["carnet"]:
            return False, "El carnet no puede quedar vacío"
        if cambios["carnet"] in carnets_registrados(excepto_id=id_estudiante):
            return False, "Ese carnet ya lo usa otro estudiante"

    registros = gestor.leer()
    posicion = buscar_posicion(registros, id_estudiante)
    if posicion is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    registros[posicion].update(cambios)
    gestor.guardar(registros)
    return True, f"Estudiante {id_estudiante} actualizado"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()

    quedan = []
    for registro in registros:
        if registro["id"] != id_estudiante:
            quedan.append(registro)

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== NOTAS Y MATERIAS =====================

def agregar_nota(id_estudiante, materia, nota):
    materia = str(materia).strip().title()
    if not materia:
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número"

    if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
        return False, f"La nota debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}"

    if nota == int(nota):
        nota = int(nota)

    registros = gestor.leer()
    posicion = buscar_posicion(registros, id_estudiante)
    if posicion is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    estudiante = Estudiante.desde_diccionario(registros[posicion])
    estudiante.agregar_nota(materia, nota)
    registros[posicion] = estudiante.a_diccionario()

    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"

    return True, f"Nota {nota} registrada en {materia}"


def promedio_de(id_estudiante):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    return True, estudiante.obtener_promedio()


def promedio_por_materia(id_estudiante):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    promedios = {}
    for materia in sorted(estudiante.notas):
        promedios[materia] = estudiante.promedio_de_materia(materia)
    return True, promedios


def materias_ofertadas():
    ofertadas = set()
    for registro in gestor.leer():
        for materia in registro.get("materias", []):
            ofertadas.add(materia)
    return ofertadas


def estudiantes_por_materia():
    agrupados = {}
    for registro in gestor.leer():
        for materia in registro.get("materias", []):
            if materia not in agrupados:
                agrupados[materia] = []
            agrupados[materia].append(registro["nombre"])
    return agrupados


def estudiantes_en_comun(id_a, id_b):
    if id_a == id_b:
        return False, "Debe comparar dos estudiantes distintos"

    estudiante_a = obtener_por_id(id_a)
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"

    estudiante_b = obtener_por_id(id_b)
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    return True, estudiante_a.materias_en_comun(estudiante_b)


# ===================== ESTADISTICAS =====================

def estadisticas():
    registros = gestor.leer()

    dominios = set()
    sin_notas = []
    for registro in registros:
        if "@" in registro["email"]:
            dominios.add(registro["email"].split("@")[1].lower())
        if not registro["notas"]:
            sin_notas.append(registro["nombre"])

    return {
        "total": len(registros),
        "materias": sorted(materias_ofertadas()),
        "dominios": sorted(dominios),
        "sin_notas": sin_notas,
    }
