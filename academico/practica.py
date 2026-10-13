from models import ModeloBase, Persona, Estudiante, Materia, Matricula


# ===================== Ejercicio 1 · Quitar duplicados conservando el orden =====================

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()
unicas = []
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print("Ejercicio 1")
print("  ciudades:", ciudades)
print("  sin repetir:", unicas)
print()


# ===================== Ejercicio 2 · Contar con un diccionario =====================

conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1

mas_repetida = max(conteo, key=conteo.get)

print("Ejercicio 2")
print("  conteo:", conteo)
print("  la mas repetida:", mas_repetida)
print()


# ===================== Ejercicio 3 · Conjuntos en accion =====================

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)

print("Ejercicio 3")
print("  en las dos:", sorted(ambas))
print("  solo en matematica:", sorted(solo_mate))
print("  estudiantes distintos:", total)
print()


# ===================== Ejercicio 4 · De lista de diccionarios a indice =====================

clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]

indice = {}
for cliente in clientes:
    indice[cliente["id"]] = cliente

print("Ejercicio 4")
print("  indice:", indice)
print("  nombre del id 2:", indice[2]["nombre"])
print()


# ===================== Ejercicio 5 · Tuplas como registros inmutables =====================

ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]

total_ventas = 0
mejor_mes = ""
mejor_monto = 0
for mes, monto in ventas:
    total_ventas = total_ventas + monto
    if monto > mejor_monto:
        mejor_mes = mes
        mejor_monto = monto

print("Ejercicio 5")
print(f"  Total: {total_ventas}")
print(f"  Mejor mes: {mejor_mes} con {mejor_monto}")
for mes, monto in ventas:
    print(f"  {mes:<10} {monto}")
print()


# ===================== Ejercicio 6 · Sobre el proyecto =====================

print("Ejercicio 6")
print("  esta en views.py: EstudianteController.estudiantes_por_carrera()")
print("  y en el menu Estudiantes, opcion 7")
print()


# ===================== Ejercicio 7 · Instancia, de clase o estatico =====================

clasificacion = {
    "a) calcular el total de una venta": "de instancia: usa self.cantidad y self.precio_unitario de esa venta",
    "b) crear un Producto desde un diccionario": "de clase: todavia no hay objeto y se arma con cls(...)",
    "c) saber si un precio es valido": "estatico: la regla no depende de ningun producto",
    "d) saber si un producto tiene stock bajo": "de instancia: compara self.stock con STOCK_MINIMO",
    "e) calcular el IVA de cualquier monto": "estatico: recibe un monto y devuelve otro, sin usar ningun producto",
}

print("Ejercicio 7")
for metodo, tipo in clasificacion.items():
    print(f"  {metodo}")
    print(f"      {tipo}")
print()


# ===================== Ejercicio 8 · Un modelo nuevo con herencia =====================

class Proveedor(Persona):

    def __init__(self, id_registro, nombre, apellido, email, ruc="", empresa=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc = ruc
        self.empresa = empresa

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc"] = self.ruc
        datos["empresa"] = self.empresa
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.empresa or 'sin empresa'} · RUC {self.ruc}"


proveedor = Proveedor.desde_diccionario({"id": 1, "nombre": "Luis", "apellido": "Mora",
                                         "email": "luis@x.com", "ruc": "0912345678001",
                                         "empresa": "Importadora Sur"})

print("Ejercicio 8")
print(" ", proveedor)
print()


# ===================== Ejercicio 9 · Polimorfismo sin if =====================

def describir(objeto):
    return objeto.etiqueta()


estudiante = Estudiante(1, "Ana", "Pérez", "ana@u.edu", "EST2026001", "Software")
materia = Materia(1, "Cálculo I", "MAT101", 4, 30)
matricula = Matricula(1, 1, 1, "2026-1", 16.5)

print("Ejercicio 9")
for objeto in (estudiante, materia, matricula, proveedor):
    print(" ", describir(objeto))
print()


# ===================== Ejercicio 10 · Atributo estatico nuevo =====================

class Producto(ModeloBase):

    DESCUENTO_MAYORISTA = 0.10
    CANTIDAD_MAYORISTA = 12

    def __init__(self, id_registro, nombre, precio, stock=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    @staticmethod
    def precio_mayorista(precio, cantidad):
        if cantidad >= Producto.CANTIDAD_MAYORISTA:
            return round(precio * (1 - Producto.DESCUENTO_MAYORISTA), 2)
        return round(precio, 2)


print("Ejercicio 10")
print("  5 unidades a 25.5 :", Producto.precio_mayorista(25.5, 5))
print("  12 unidades a 25.5:", Producto.precio_mayorista(25.5, 12))
print("  descuento:", Producto.DESCUENTO_MAYORISTA, "desde", Producto.CANTIDAD_MAYORISTA, "unidades")
