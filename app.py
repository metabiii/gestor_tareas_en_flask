from flask import Flask, render_template, request, redirect
import webbrowser
from gestor_tareas import cargar_tareas, agregar_tarea, completar_tarea, eliminar_tarea

app = Flask(__name__)

@app.route('/')
def index():
    tareas = cargar_tareas()
    return render_template("index.html", tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get("titulo")
    if titulo:
        agregar_tarea(titulo)
    return redirect("/")

@app.route('/completar/<int:indice>')
def completar(indice):
    completar_tarea(indice)
    return redirect("/")

@app.route('/eliminar/<int:indice>')
def eliminar(indice):
    eliminar_tarea(indice)
    return redirect("/")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

