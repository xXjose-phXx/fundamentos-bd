from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Guapo117",  # Coloca tu contraseña si la cambiaste
        database="cafeteria_universitaria"
    )
    return connection


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idproducto AS ID_Producto, nombre AS Nombre, categoria AS Categoria, precio AS Precio, stock AS Stock FROM Producto")
    lista_productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=lista_productos)

@app.route('/pedidos')
def pedidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT
            p.idpedido AS ID_Pedido,
            c.nombre AS Cliente,
            p.fecha_pedido AS Fecha,
            p.estado AS Estado,
            SUM(CAST(dp.cantidad AS DECIMAL(10,2)) * CAST(dp.precio_unitario AS DECIMAL(10,2))) AS Total
        FROM Pedido p
        JOIN Cliente c ON p.cliente_idcliente = c.idcliente
        JOIN Detalle_Pedido dp ON p.idpedido = dp.pedido_idpedido
        GROUP BY p.idpedido, c.nombre, p.fecha_pedido, p.estado
    """
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pedidos.html', pedidos=lista_pedidos)


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Producto (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)", (nombre, categoria, precio, stock))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/productos')
    return render_template('agregar_producto.html')


@app.route('/agregar_pedido', methods=['GET', 'POST'])
def agregar_pedido():
    if request.method == 'POST':
        id_cliente = request.form['cliente_idcliente']
        fecha = request.form['fecha']
        estado = request.form['estado']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Pedido (cliente_idcliente, fecha_pedido, estado) VALUES (%s, %s, %s)",
            (id_cliente, fecha, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/pedidos')
    return render_template('agregar_pedido.html')



@app.route('/actualizar_producto/<int:id_producto>', methods=['GET', 'POST'])
def actualizar_producto(id_producto):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        cursor.execute("UPDATE Producto SET nombre = %s, categoria = %s, precio = %s, stock = %s WHERE idproducto = %s",
               (nombre, categoria, precio, stock, id_producto))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/productos')

    cursor.execute("SELECT * FROM Producto WHERE idproducto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('actualizar_producto.html', p=producto)


@app.route('/actualizar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def actualizar_pedido(id_pedido):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_cliente = request.form['cliente_idcliente']
        fecha_pedido = request.form['fecha']
        estado = request.form['estado']

        cursor.execute("UPDATE Pedido SET cliente_idcliente = %s, fecha_pedido = %s, estado = %s WHERE idpedido = %s",
                       (id_cliente, fecha_pedido, estado, id_pedido))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/pedidos')

    cursor.execute("SELECT * FROM Pedido WHERE idpedido = %s", (id_pedido,))
    pedido = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('actualizar_pedido.html', p=pedido)


@app.route('/borrar_producto/<int:id_producto>', methods=['POST'])
def borrar_producto(id_producto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Producto WHERE idproducto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/productos')


@app.route('/borrar_pedido/<int:id_pedido>', methods=['POST'])
def borrar_pedido(id_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pedido WHERE idpedido = %s", (id_pedido,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/pedidos')


if __name__ == '__main__':
    app.run(debug=True)
