from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",        # cámbialo según tu usuario
    password="",        # agrega tu contraseña
    database="desarrollo_web"
)
cursor = conexion.cursor(dictionary=True)

# Ruta principal: listar productos
@app.route('/')
@app.route('/productos')
def productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return render_template("index.html", productos=productos)

# Crear producto
@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                       (nombre, precio, stock))
        conexion.commit()
        return redirect(url_for('productos'))
    return render_template("crear.html")

# Editar producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
                       (nombre, precio, stock, id))
        conexion.commit()
        return redirect(url_for('productos'))
    return render_template("editar.html", producto=producto)

# Eliminar producto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()
    return redirect(url_for('productos'))

if __name__ == '__main__':
    app.run(debug=True)
