import json
import os

DATA_FILE = "data/tareas.json"
os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def cargar_tareas():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as f:
        json.dump(tareas, f, indent=4)

def agregar_tarea(titulo):
    tareas = cargar_tareas()
    tareas.append({"titulo": titulo, "estado": "pendiente"})
    guardar_tareas(tareas)

def completar_tarea(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas[indice]["estado"] = "completada"
        guardar_tareas(tareas)

def eliminar_tarea(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
        guardar_tareas(tareas)
