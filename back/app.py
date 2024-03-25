from flask import Flask, request, jsonify, render_template
import os
import sqlite3

pp = Flask(__name__, static_folder='form/static', template_folder='form/templates')

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

    # Responder al usuario con un mensaje de confirmación
    return render_template('saludo.html', name=form_data['name'])
# Función para guardar los datos en la base de datos


def save_to_database(data):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO form_data (name, email, subject, message) 
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['email'], data['subject'], data['message']))
        db.commit()


if __name__ == '__main__':
    app.run(debug=True)
