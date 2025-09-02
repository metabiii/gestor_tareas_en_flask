import json
import os
from datetime import datetime

ARCHIVO_TAREAS = "tareas.json"
ARCHIVO_HISTORIAL = "historial_tareas.json"

# ----------------- Clase Tarea -----------------
class Tarea:
    def __init__(self, nombre, prioridad, vencimiento, completada=False):
        self.nombre = nombre
        self.prioridad = prioridad
        self.vencimiento = vencimiento
        self.completada = completada

    def marcar_completada(self):
        self.completada = True

    def descripcion(self):
        estado = "Completada" if self.completada else "Pendiente"
        return f"{self.nombre} | Prioridad: {self.prioridad} | Vence: {self.vencimiento} | Estado: {estado}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "prioridad": self.prioridad,
            "vencimiento": self.vencimiento,
            "completada": self.completada
        }

    @staticmethod
    def from_dict(data):
        return Tarea(data["nombre"], data["prioridad"], data["vencimiento"], data["completada"])

# ----------------- Funciones de Tareas -----------------
def agregar_tarea():
    nombre = input("Nombre de la tarea: ")

    while True:
        prioridad = input("Prioridad (alta/media/baja): ").lower()
        if prioridad in ["alta", "media", "baja"]:
            break
        print("Prioridad inválida. Intenta de nuevo.")

    vencimiento = input("Fecha de vencimiento (dd/mm/yyyy): ")
    return Tarea(nombre, prioridad, vencimiento)

def guardar_tareas_json(tareas):
    try:
        with open(ARCHIVO_TAREAS, "w") as f:
            json.dump([t.to_dict() for t in tareas], f, indent=4)
        print("Tareas guardadas correctamente en JSON.")
    except Exception as e:
        print(f"Error al guardar tareas: {e}")

def leer_tareas_json():
    tareas = []
    if not os.path.exists(ARCHIVO_TAREAS):
        return tareas
    try:
        with open(ARCHIVO_TAREAS, "r") as f:
            data = json.load(f)
            for item in data:
                tareas.append(Tarea.from_dict(item))
    except Exception as e:
        print(f"Error al leer tareas: {e}")
    return tareas

def marcar_tarea_completada(tarea):
    tarea.marcar_completada()
    guardar_historial(tarea)
    print(f"Tarea '{tarea.nombre}' completada y registrada en historial.")

def guardar_historial(tarea):
    historial = []
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r") as f:
                historial = json.load(f)
        except Exception as e:
            print(f"Error al leer historial: {e}")
    historial.append(tarea.to_dict())
    try:
        with open(ARCHIVO_HISTORIAL, "w") as f:
            json.dump(historial, f, indent=4)
    except Exception as e:
        print(f"Error al guardar historial: {e}")

def mostrar_historial():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("No hay historial de tareas completadas.")
        return
    try:
        with open(ARCHIVO_HISTORIAL, "r") as f:
            historial = json.load(f)
            print("\n📜 Historial de tareas completadas:")
            for t in historial:
                estado = "Completada"
                print(f"{t['nombre']} | Prioridad: {t['prioridad']} | Vence: {t['vencimiento']} | Estado: {estado}")
    except Exception as e:
        print(f"Error al leer historial: {e}")

def mostrar_recordatorio(tareas):
    hoy = datetime.today().strftime("%d/%m/%Y")
    print("\n📌 Tareas que vencen hoy:")
    hay = False
    for t in tareas:
        if t.vencimiento == hoy and not t.completada:
            print(t.descripcion())
            hay = True
    if not hay:
        print("No hay tareas urgentes para hoy.")

def mostrar_tareas(tareas, filtro=None):
    if not tareas:
        print("No hay tareas.")
        return
    hoy = datetime.today().strftime("%d/%m/%Y")
    for t in tareas:
        mostrar = True
        if filtro:
            if "prioridad" in filtro and t.prioridad != filtro["prioridad"]:
                mostrar = False
            if "vence_hoy" in filtro and t.vencimiento != hoy:
                mostrar = False
        if mostrar:
            print(t.descripcion())

def ordenar_tareas(tareas, criterio="prioridad"):
    if criterio == "prioridad":
        prioridad_valor = {"alta": 1, "media": 2, "baja": 3}
        tareas.sort(key=lambda x: prioridad_valor[x.prioridad])
    elif criterio == "vencimiento":
        tareas.sort(key=lambda x: datetime.strptime(x.vencimiento, "%d/%m/%Y"))

def buscar_tareas(tareas, palabra_clave):
    resultados = []
    for t in tareas:
        if palabra_clave.lower() in t.nombre.lower():
            resultados.append(t)
    return resultados

def editar_tarea(tarea):
    print(f"Tarea actual: {tarea.descripcion()}")
    nuevo_nombre = input("Nuevo nombre (enter para no cambiar): ")
    if nuevo_nombre.strip():
        tarea.nombre = nuevo_nombre
    nueva_prioridad = input("Nueva prioridad (alta/media/baja) (enter para no cambiar): ").lower()
    if nueva_prioridad in ["alta", "media", "baja"]:
        tarea.prioridad = nueva_prioridad
    nueva_fecha = input("Nueva fecha de vencimiento (dd/mm/yyyy) (enter para no cambiar): ")
    if nueva_fecha.strip():
        tarea.vencimiento = nueva_fecha
    print("Tarea actualizada:")
    print(tarea.descripcion())

# ----------------- Menú Principal -----------------
tareas = leer_tareas_json()
mostrar_recordatorio(tareas)

while True:
    print("\nOpciones:")
    print("1. Agregar tarea")
    print("2. Marcar tarea completada")
    print("3. Mostrar todas las tareas")
    print("4. Mostrar tareas filtradas")
    print("5. Ordenar tareas")
    print("6. Guardar tareas")
    print("7. Salir")
    print("8. Buscar tareas")
    print("9. Editar tareas")
    print("10. Ver historial de tareas completadas")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        tarea = agregar_tarea()
        tareas.append(tarea)
        print(f"Tarea '{tarea.nombre}' agregada.")
    elif opcion == "2":
        for i, t in enumerate(tareas):
            print(f"{i+1}. {t.descripcion()}")
        try:
            idx = int(input("Número de la tarea a marcar como completada: ")) - 1
            marcar_tarea_completada(tareas[idx])
        except (ValueError, IndexError):
            print("Entrada inválida.")
    elif opcion == "3":
        mostrar_tareas(tareas)
    elif opcion == "4":
        print("Filtrar por: 1. Prioridad 2. Vence hoy")
        f = input("Elige filtro: ")
        if f == "1":
            prio = input("Ingresa prioridad (alta/media/baja): ").lower()
            mostrar_tareas(tareas, filtro={"prioridad": prio})
        elif f == "2":
            mostrar_tareas(tareas, filtro={"vence_hoy": True})
    elif opcion == "5":
        print("Ordenar por: 1. Prioridad 2. Fecha de vencimiento")
        c = input("Elige criterio: ")
        if c == "1":
            ordenar_tareas(tareas, "prioridad")
        elif c == "2":
            ordenar_tareas(tareas, "vencimiento")
        print("Tareas ordenadas.")
    elif opcion == "6":
        guardar_tareas_json(tareas)
    elif opcion == "7":
        guardar_tareas_json(tareas)
        print("Saliendo del programa...")
        break
    elif opcion == "8":
        palabra = input("Palabra clave para buscar: ")
        resultados = buscar_tareas(tareas, palabra)
        if resultados:
            print("Tareas encontradas:")
            for t in resultados:
                print(t.descripcion())
        else:
            print("No se encontraron tareas.")
    elif opcion == "9":
        for i, t in enumerate(tareas):
            print(f"{i+1}. {t.descripcion()}")
        try:
            idx = int(input("Número de la tarea a editar: ")) - 1
            editar_tarea(tareas[idx])
        except (ValueError, IndexError):
            print("Entrada inválida.")
    elif opcion == "10":
        mostrar_historial()
    else:
        print("Opción inválida. Intenta de nuevo.")
