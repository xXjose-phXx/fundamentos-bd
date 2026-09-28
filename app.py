import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

# conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",       # cámbialo por tu usuario
    password="Guapo117",  # cámbialo por tu contraseña
    database="cafeteria_universitaria"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("select * from producto;")
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/pedidos')
def pedidos():
    cursor = conexion.cursor(dictionary=True)
    consulta = """
        select p.idpedido, c.nombre as cliente, p.fecha_pedido, p.estado,
               sum(dp.cantidad * dp.precio_unitario) as total
        from pedido p
        join cliente c on p.cliente_idcliente = c.idcliente
        join detalle_pedido dp on dp.pedido_idpedido = p.idpedido
        group by p.idpedido, c.nombre, p.fecha_pedido, p.estado;
    """
    cursor.execute(consulta)
    pedidos = cursor.fetchall()
    return render_template('pedidos.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)