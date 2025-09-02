from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Ruta absoluta del archivo JSON
ruta_json = os.path.join(os.path.dirname(__file__), "tareas.json")

# ------------------------------
# Funciones para manejar tareas
# ------------------------------
def cargar_tareas():
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Si no existe, crear estructura inicial
        tareas = {
            "pendientes": [
                {"id": 1, "texto": "Estudiar Python"},
                {"id": 2, "texto": "Practicar con Flask"}
            ],
            "completadas": [
                {"id": 3, "texto": "Configurar entorno virtual"}
            ]
        }
        guardar_tareas(tareas)
        return tareas

def guardar_tareas(tareas):
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)

# ------------------------------
# Rutas Flask
# ------------------------------
@app.route("/")
def index():
    tareas = cargar_tareas()
    return render_template("index.html", tareas=tareas)

@app.route("/agregar", methods=["POST"])
def agregar():
    texto = request.form.get("tarea")
    if not texto:
        return redirect(url_for("index"))

    tareas = cargar_tareas()
    nuevo_id = max([t["id"] for t in tareas["pendientes"] + tareas["completadas"]], default=0) + 1
    tareas["pendientes"].append({"id": nuevo_id, "texto": texto})
    guardar_tareas(tareas)
    return redirect(url_for("index"))

@app.route("/completar/<int:id>")
def completar(id):
    tareas = cargar_tareas()
    for t in tareas["pendientes"]:
        if t["id"] == id:
            tareas["pendientes"].remove(t)
            tareas["completadas"].append(t)
            break
    guardar_tareas(tareas)
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id>")
def eliminar(id):
    tareas = cargar_tareas()
    for lista in ["pendientes", "completadas"]:
        for t in tareas[lista]:
            if t["id"] == id:
                tareas[lista].remove(t)
                break
    guardar_tareas(tareas)
    return redirect(url_for("index"))

# ------------------------------
# Ejecutar app
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
