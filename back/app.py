from flask import Flask, request, render_template, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(__file__)

# Configuración de la base de datos
DATABASE = os.path.join(current_dir, 'Api_MV.db')

# Función para conectar a la base de datos
def connect_db():
    return sqlite3.connect(DATABASE)

# Crear la tabla si no existe
def init_db():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS form_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        db.commit()

# Inicializar la base de datos
init_db()

# Ruta para manejar la solicitud POST del formulario
@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Recibir los datos del formulario
    form_data = request.form

    # Guardar los datos en la base de datos
    save_to_database(form_data)

    # Redirigir al usuario con un mensaje de agradecimiento
    return redirect(url_for('Gracias por completar el formulario', name=form_data['name']))

# Función para guardar los datos en la base de datos
def save_to_database(data):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO form_data (name, email, subject, message) 
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['email'], data['subject'], data['message']))
        db.commit()

# Ruta para mostrar mensaje de agradecimiento
@app.route('/gracias')
def gracias():
    name = request.args.get('name')
    return render_template('..\\index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
