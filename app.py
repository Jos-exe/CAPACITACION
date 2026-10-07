from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bd_veterinaria.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/clientes")
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nombre, telefono) VALUES (?, ?)', (nombre, telefono))
        conn.commit()
        conn.close()
        return redirect(url_for('clientes'))
        
    return render_template('form_cliente.html')

@app.route("/servicios")
def servicios():
    conn = get_db_connection()
    servicios = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    return render_template('servicios.html', servicios=servicios)

@app.route('/servicios/nuevo', methods=('GET', 'POST'))
def nuevo_servicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        conn = get_db_connection()
        conn.execute('INSERT INTO servicios (nombre, precio) VALUES (?, ?)', (nombre, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('servicios'))
    return render_template('form_servicio.html')

@app.route("/")
@app.route("/citas")
def citas():
    conn = get_db_connection()
    citas = conn.execute('''
        SELECT i.id, i.fecha, e.nombre as cliente, c.nombre as servicio 
        FROM citas i
        JOIN clientes e ON i.cliente_id = e.id
        JOIN servicios c ON i.servicio_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('citas.html', citas=citas)

@app.route('/citas/nuevo', methods=('GET', 'POST'))
def nueva_cita():
    conn = get_db_connection()
    if request.method == 'POST':
        fecha = request.form['fecha']
        cliente_id = request.form['cliente_id']
        servicio_id = request.form['servicio_id']
        
        conn.execute('INSERT INTO citas (fecha, cliente_id, servicio_id) VALUES (?, ?, ?)', 
                     (fecha, cliente_id, servicio_id))
        conn.commit()
        conn.close()
        return redirect(url_for('citas'))
    
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    servicios = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    return render_template('form_cita.html', clientes=clientes, servicios=servicios)

@app.route('/citas/eliminar/<int:id>', methods=('POST',))
def eliminar_cita(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM citas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('citas'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        
        conn.execute('UPDATE clientes SET nombre = ?, telefono = ? WHERE id = ?', 
                     (nombre, telefono, id))
        conn.commit()
        conn.close()
        return redirect(url_for('clientes'))
        
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('form_cliente.html', cliente=cliente)

@app.route('/servicios/editar/<int:id>', methods=['GET', 'POST'])
def editar_servicio(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        
        conn.execute('UPDATE servicios SET nombre = ?, precio = ? WHERE id = ?', 
                     (nombre, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('servicios'))
        
    servicio = conn.execute('SELECT * FROM servicios WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('form_servicio.html', servicio=servicio)

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))


@app.route('/servicios/eliminar/<int:id>')
def eliminar_servicio(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM servicios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('servicios'))

if __name__ == '__main__':
    app.run(debug=True)