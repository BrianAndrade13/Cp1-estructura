CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")  # tupla porque los campos nunca cambian


class Estudiante:

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self.notas = notas if notas else {}  # dict porque busco las notas por nombre de materia
        self.materias = set(materias) if materias else set()  # set porque no se pueden repetir

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        if materia not in self.notas:
            self.notas[materia] = []
        self.notas[materia].append(nota)

    def obtener_promedio(self):
        todas = []
        for lista_notas in self.notas.values():
            for nota in lista_notas:
                todas.append(nota)

        if not todas:
            return 0
        return round(sum(todas) / len(todas), 2)

    def promedio_de_materia(self, materia):
        lista_notas = self.notas.get(materia, [])
        if not lista_notas:
            return 0
        return round(sum(lista_notas) / len(lista_notas), 2)

    def materias_en_comun(self, otro_estudiante):
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"
