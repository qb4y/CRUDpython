from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# ----- CONNECT DB
mysql = MySQL()
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "2212"
app.config["MYSQL_DB"] = "CRUDpython"
mysql.init_app(app)  # Initialize
# -----

CARPETA = os.path.join("templates/uploads")
app.config["CARPETA"] = CARPETA


@app.route("/templates/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config["CARPETA"], nombreFoto)


# ----- MENU
@app.route("/")
def index():
    sql = "SELECT * FROM Empleados;"
    cursor = mysql.connection.cursor()
    cursor.execute(sql)

    empleados = cursor.fetchall()
    # print(empleados) # Mostrar en consola

    mysql.connection.commit()
    return render_template("empleados/index.html", empleados=empleados)


# -----


# ----- DELETE
@app.route("/destroy/<int:id>")
def destroy(id):
    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM Empleados WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect("/")


# -----


# ----- EDIT
@app.route("/edit/<int:id>")
def edit(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Empleados WHERE id=%s", (id,))
    empleados = cursor.fetchall()
    mysql.connection.commit()

    return render_template("empleados/edit.html", empleados=empleados)


# -----


# ----- UPDATE
@app.route("/update", methods=["POST"])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    id = request.form["txtID"]

    sql = "UPDATE Empleados SET nombre=%s, correo=%s WHERE id=%s;"

    datos = (_nombre, _correo, id)

    cursor = mysql.connection.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y-%H-%M-%S")

    if _foto.filename != "":
        nuevoNombreFoto = tiempo + "_" + _foto.filename
        _foto.save("templates/uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT foto FROM Empleados WHERE id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config["CARPETA"], fila[0][0]))
        cursor.execute(
            "UPDATE Empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id)
        )
        mysql.connection.commit()

    cursor.execute(sql, datos)
    mysql.connection.commit()

    return redirect("/")


# -----


# ----- CREATE
@app.route("/create")
def create():
    return render_template("empleados/create.html")


# -----


# ----- STORE
@app.route("/store", methods=["POST"])
def storage():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    now = datetime.now()
    tiempo = now.strftime("%Y-%H-%M-%S")

    if _foto.filename != "":
        nuevoNombreFoto = tiempo + "_" + _foto.filename
        _foto.save("templates/uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO Empleados (id, nombre, correo, foto) VALUES (NULL, %s, %s, %s);"

    datos = (_nombre, _correo, nuevoNombreFoto)

    cursor = mysql.connection.cursor()
    cursor.execute(sql, datos)
    mysql.connection.commit()
    return redirect("/")


# -----

# ----- DEBUG RUN
if __name__ == "__main__":
    app.run(debug=True)
# -----
