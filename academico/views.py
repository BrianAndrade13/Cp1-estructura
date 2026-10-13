import os
from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

CARPETA = os.path.dirname(os.path.abspath(__file__))


class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


class EstudianteController(CrudBase):

    # tupla: son campos fijos que nunca cambian, igual que el retorno (exito, mensaje)
    CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet", "carrera")

    def __init__(self, archivo=os.path.join(CARPETA, "data", "estudiantes.json")):
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        for campo in self.CAMPOS_OBLIGATORIOS:
            if campo in datos or id_actual is None:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            usados = set()
            for estudiante in self.lista:
                if estudiante.id != id_actual:
                    usados.add(estudiante.email)
            if email in usados:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            # conjunto: preguntar si el carnet ya existe es inmediato y no admite repetidos
            carnets = set()
            for estudiante in self.lista:
                if estudiante.id != id_actual:
                    carnets.add(estudiante.carnet.upper())
            if carnet in carnets:
                return "Ese carnet ya está registrado"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_estudiante):
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for estudiante in self.lista:
            for campo in self.CAMPOS_BUSCABLES:
                if texto in str(getattr(estudiante, campo)).lower():
                    encontrados.append(estudiante)
                    break
        return encontrados

    def siguiente(self):
        mayor = 0
        for estudiante in self.lista:
            if estudiante.id > mayor:
                mayor = estudiante.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(self.siguiente(),
                                str(datos["nombre"]).strip().title(),
                                str(datos["apellido"]).strip().title(),
                                str(datos["email"]).strip().lower(),
                                str(datos["carnet"]).strip().upper(),
                                str(datos.get("carrera", "")).strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indicó ningún cambio"

        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_estudiante)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"Estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"

    def carreras(self):
        unicas = set()
        for estudiante in self.lista:
            if estudiante.carrera != "":
                unicas.add(estudiante.carrera)
        return sorted(unicas)

    def estudiantes_por_carrera(self):
        agrupados = {}
        for estudiante in self.lista:
            carrera = estudiante.carrera or "Sin carrera"
            if carrera not in agrupados:
                agrupados[carrera] = []
            agrupados[carrera].append(estudiante.nombre)
        return agrupados


class MateriaController(CrudBase):

    CAMPOS_OBLIGATORIOS = ("nombre", "codigo", "creditos", "cupos")
    CAMPOS_BUSCABLES = ("nombre", "codigo")

    def __init__(self, archivo=os.path.join(CARPETA, "data", "materias.json")):
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        for campo in self.CAMPOS_OBLIGATORIOS:
            if campo in datos or id_actual is None:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            # conjunto: así se sabe al instante si el código ya existe
            codigos = set()
            for materia in self.lista:
                if materia.id != id_actual:
                    codigos.add(materia.codigo.upper())
            if codigo in codigos:
                return f"Ya existe una materia con el código {codigo}"

        if "creditos" in datos:
            try:
                creditos = int(str(datos["creditos"]).strip())
            except ValueError:
                return "Los créditos deben ser un número entero"
            if creditos < 1 or creditos > 10:
                return "Los créditos deben estar entre 1 y 10"

        if "cupos" in datos:
            try:
                cupos = int(str(datos["cupos"]).strip())
            except ValueError:
                return "Los cupos deben ser un número entero"
            if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
                return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_materia):
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontradas = []
        if texto == "":
            return encontradas

        for materia in self.lista:
            for campo in self.CAMPOS_BUSCABLES:
                if texto in str(getattr(materia, campo)).lower():
                    encontradas.append(materia)
                    break
        return encontradas

    def siguiente(self):
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = Materia(self.siguiente(),
                          str(datos["nombre"]).strip().title(),
                          str(datos["codigo"]).strip().upper(),
                          int(datos["creditos"]),
                          int(datos["cupos"]))
        self.lista.append(materia)
        self.guardar()
        return True, f"Materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        if not datos:
            return False, "No se indicó ningún cambio"

        permitidos = {"nombre", "codigo", "creditos", "cupos"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"

        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    def materias_sin_cupo(self):
        sin_cupo = []
        for materia in self.lista:
            if not materia.hay_cupo():
                sin_cupo.append(materia)
        return sin_cupo


class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo=os.path.join(CARPETA, "data", "matriculas.json")):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "estudiante_id y materia_id deben ser números enteros"

        periodo = str(datos.get("periodo", "")).strip()
        if periodo == "":
            return "El campo periodo es obligatorio"

        # conjunto: saber si un id existe es inmediato
        ids_estudiantes = set()
        for estudiante in self.estudiantes.leer():
            ids_estudiantes.add(estudiante.id)
        if estudiante_id not in ids_estudiantes:
            return f"No existe un estudiante con id {estudiante_id}"

        materia = self.materias.obtener(materia_id)
        if materia is None:
            return f"No existe una materia con id {materia_id}"
        if not materia.hay_cupo():
            return f"La materia {materia.nombre} no tiene cupos disponibles"

        for matricula in self.lista:
            if (matricula.estudiante_id == estudiante_id
                    and matricula.materia_id == materia_id
                    and matricula.periodo == periodo):
                return "El estudiante ya está matriculado en esa materia en ese periodo"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def buscar(self, texto):
        texto = texto.strip()
        encontradas = []
        if texto == "":
            return encontradas

        for matricula in self.lista:
            if texto in matricula.periodo:
                encontradas.append(matricula)
        return encontradas

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        matricula = Matricula(self.siguiente(),
                              int(datos["estudiante_id"]),
                              materia.id,
                              str(datos["periodo"]).strip())

        materia.ocupar_cupo()
        self.materias.guardar()
        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula {matricula.id} registrada en {materia.nombre}"

    def actualizar(self, id_matricula, datos):
        return False, "Las matrículas no se modifican: registre la nota o retire la matrícula"

    def eliminar(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_matricula} retirada y cupo devuelto"

    def registrar_nota(self, id_matricula, nota):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        nota = str(nota).strip().replace(",", ".")
        if not Materia.es_nota_valida(nota):
            return False, "La nota debe ser un número entre 0 y 20"

        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota {matricula.nota} registrada. Estado: {matricula.estado()}"

    def certificado(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return None

        # diccionario índice {id: objeto}: se busca por id sin recorrer la lista
        indice_estudiantes = {}
        for estudiante in self.estudiantes.leer():
            indice_estudiantes[estudiante.id] = estudiante
        indice_materias = {}
        for materia in self.materias.leer():
            indice_materias[materia.id] = materia

        estudiante = indice_estudiantes.get(matricula.estudiante_id)
        materia = indice_materias.get(matricula.materia_id)

        if estudiante is None:
            datos_estudiante = "eliminado"
        else:
            datos_estudiante = f"{estudiante.nombre_completo()} ({estudiante.carnet})"

        if materia is None:
            datos_materia = "eliminada"
        else:
            datos_materia = f"{materia.nombre} ({materia.codigo}) · {materia.creditos} créditos"

        if matricula.nota is None:
            nota = "sin registrar"
        else:
            nota = matricula.nota

        texto = f"CERTIFICADO #{matricula.id} periodo: {matricula.periodo}\n"
        texto += f"Estudiante: {datos_estudiante}\n"
        texto += f"Materia : {datos_materia}\n"
        texto += "-" * 42 + "\n"
        texto += f"Nota : {nota}\n"
        texto += f"Estado : {matricula.estado()}"
        return texto

    def matriculas_por_estudiante(self):
        # diccionario de listas: cada estudiante guarda varias matrículas
        agrupadas = {}
        for matricula in self.lista:
            if matricula.estudiante_id not in agrupadas:
                agrupadas[matricula.estudiante_id] = []
            agrupadas[matricula.estudiante_id].append(matricula)
        return agrupadas

    def promedio_de_estudiante(self, id_estudiante):
        suma = 0
        cantidad = 0
        for matricula in self.lista:
            if matricula.estudiante_id == id_estudiante and matricula.nota is not None:
                suma += matricula.nota
                cantidad += 1

        if cantidad == 0:
            return None
        return round(suma / cantidad, 2)

    def cantidad_aprobadas(self):
        aprobadas = 0
        for matricula in self.lista:
            if matricula.esta_aprobada():
                aprobadas += 1
        return aprobadas
