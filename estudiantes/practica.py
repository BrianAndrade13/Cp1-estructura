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
