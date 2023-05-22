import json
from flask import Flask, jsonify, request
from pydal import DAL, Field
from datetime import datetime, timedelta

db = DAL('postgres://usuario:password@localhost:5432/usuarios')

#Definiar la tabla Usuario
db.define_table('usuario',
                Field('cedula_identidad', 'id', unique=True),
                Field('nombre', 'string'),
                Field('primer_apellido', 'string'),
                Field('segundo_apellido', 'string'),
                Field('fecha_nacimiento', 'date'))

app = Flask(__name__)

# Endpoint para pagina Inicio
@app.route('/')
def inicio():
	return 'hello'

# Endpoint para crear un usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
	if request.is_json:
		data = request.get_json()        
		cedula_identidad = data.get('cedula_identidad')
		nombre = data.get('nombre')
		primer_apellido = data.get('primer_apellido')
		segundo_apellido = data.get('segundo_apellido')
		fecha_nacimiento = data.get('fecha_nacimiento')
	else:
		cedula_identidad = request.form.get('cedula_identidad')
		nombre = request.form.get('nombre')
		primer_apellido = request.form.get('primer_apellido')
		segundo_apellido = request.form.get('segundo_apellido')
		fecha_nacimiento = request.form.get('fecha_nacimiento')
    
	db.usuario.insert(cedula_identidad = cedula_identidad, 
						nombre=nombre, 
						primer_apellido=primer_apellido, 
						segundo_apellido=segundo_apellido, 
						fecha_nacimiento=fecha_nacimiento)
	db.commit();
	return jsonify({'mensaje': 'Usuario creado exitosamente'})

# Endpoint para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
	usuario = db(db.usuario).select()
	data=[]
	for row in usuario:
		data.append({'cedula_identidad': row.cedula_identidad, 'nombre': row.nombre, 'primer_apellido': row.primer_apellido, 'segundo_apellido': row.segundo_apellido, 'fecha_nacimiento': row.fecha_nacimiento.isoformat()})
	json_data = json.dumps(data)
	return jsonify(json_data)

# Endpoint para obtener un usuario específico segun cedula de identidad
@app.route('/usuarios/<int:cedula_identidad>', methods=['GET'])
def obtener_usuario(cedula_identidad):
	usuario = db(db.usuario.cedula_identidad == cedula_identidad).select()
	if usuario:
		data=[]
		for row in usuario:
			data.append({'cedula_identidad': row.cedula_identidad, 'nombre': row.nombre, 'primer_apellido': row.primer_apellido, 'segundo_apellido': row.segundo_apellido, 'fecha_nacimiento': row.fecha_nacimiento.isoformat()})
		json_data = json.dumps(data)
		return jsonify(json_data)
	else:
		return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Endpoint para actualizar los datos de un usuario segun cedula de Identidad
@app.route('/usuarios/<int:cedula_identidad>', methods=['PUT'])
def actualizar_usuario(cedula_identidad):
	usuario = db(db.usuario.cedula_identidad == cedula_identidad).select().first()
	if usuario:
		if request.is_json:
			data = request.get_json()        			
			nombre = data.get('nombre')
			primer_apellido = data.get('primer_apellido')
			segundo_apellido = data.get('segundo_apellido')
			fecha_nacimiento = data.get('fecha_nacimiento')
		else:			
			nombre = request.form.get('nombre')
			primer_apellido = request.form.get('primer_apellido')
			segundo_apellido = request.form.get('segundo_apellido')
			fecha_nacimiento = request.form.get('fecha_nacimiento')
		usuario.update_record(	nombre=nombre, 
								primer_apellido=primer_apellido, 
								segundo_apellido=segundo_apellido, 
								fecha_nacimiento=fecha_nacimiento)
		db.commit();
		return jsonify({'mensaje': 'Usuario actualizado exitosamente'})
	else:
		return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Endpoint para eliminar un usuario por cedula de Identidad
@app.route('/usuarios/<int:cedula_identidad>', methods=['DELETE'])
def eliminar_usuario(cedula_identidad):
	usuario = db(db.usuario.cedula_identidad == cedula_identidad).select().first()
	if usuario:
		db(db.usuario.cedula_identidad == cedula_identidad).delete()
		db.commit();
		return jsonify({'mensaje': 'Usuario eliminado exitosamente'})
	else:
		return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Endpoint para mostrar el promedio de edades de los usuarios
@app.route('/usuarios/promedio-edad', methods=['GET'])
def promedio_edad():
	usuario = db(db.usuario).select()
	ahora = datetime.now()
	suma = 0
	for row in usuario:
		fecha_nacimiento = row.fecha_nacimiento
		diferencia = ahora.year - fecha_nacimiento.year
		
		if fecha_nacimiento.month < ahora.month or (fecha_nacimiento.month == ahora.month and fecha_nacimiento.day < ahora.day):
			diferencia=diferencia-1
		suma = suma + diferencia
	promedio = suma / len(usuario)
	return jsonify({'promedio_edad': promedio})

# Endpoint para mostrar la versión del API REST
@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({"nameSystem": "api-users", "version": "0.0.1", "developer":"Erwin Saul Serrudo Condori", "email": "mackonkey@gmail.com"})

if __name__ == '__main__':
    app.run()
