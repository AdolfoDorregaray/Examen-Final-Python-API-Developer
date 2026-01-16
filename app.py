import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 1. MODELO DE BASE DE DATOS ---
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    aprobado = db.Column(db.Boolean, default=False)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# --- 2. CARGA DE DATOS DESDE estudiante.json (Formato MongoDB) ---
def cargar_datos_iniciales():
    if Estudiante.query.count() == 0:
        if os.path.exists('estudiante.json'):
            with open('estudiante.json', 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
                for item in datos_json:
                    # Limpiamos el formato de MongoDB ($date)
                    fecha_str = item['fecha']['$date'].replace('Z', '')
                    fecha_dt = datetime.fromisoformat(fecha_str)
                    
                    nuevo = Estudiante(
                        nombre=item['nombre'],
                        apellido=item['apellido'],
                        aprobado=item['aprobado'],
                        nota=item['nota'],
                        fecha=fecha_dt
                    )
                    db.session.add(nuevo)
            db.session.commit()
            print(">>> Base de datos inicializada con éxito desde estudiante.json")

with app.app_context():
    db.create_all()
    cargar_datos_iniciales()

# --- 3. ENDPOINTS API REST ---

# GET /estudiantes: Lista completa
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    estudiantes = Estudiante.query.all()
    output = []
    for e in estudiantes:
        output.append({
            "id": e.id,
            "nombre": e.nombre,
            "apellido": e.apellido,
            "aprobado": e.aprobado,
            "nota": e.nota,
            "fecha": e.fecha.strftime('%Y-%m-%d')
        })
    return jsonify(output)

# GET /estudiantes/<id>: Detalle de un estudiante
@app.route('/estudiantes/<int:id>', methods=['GET'])
def get_estudiante(id):
    e = Estudiante.query.get_or_404(id)
    return jsonify({"id": e.id, "nombre": e.nombre, "nota": e.nota, "aprobado": e.aprobado})

# POST /estudiantes: Crear nuevo
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    nuevo = Estudiante(
        nombre=data['nombre'],
        apellido=data['apellido'],
        nota=data['nota'],
        aprobado=data.get('aprobado', data['nota'] >= 10.5), # Lógica de aprobación
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante creado", "id": nuevo.id}), 201

# PUT /estudiantes/<id>: Actualizar
@app.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    e = Estudiante.query.get_or_404(id)
    data = request.get_json()
    
    e.nombre = data.get('nombre', e.nombre)
    e.apellido = data.get('apellido', e.apellido)
    e.nota = data.get('nota', e.nota)
    e.aprobado = e.nota >= 10.5
    
    db.session.commit()
    return jsonify({"mensaje": "Datos actualizados correctamente"})

# DELETE /estudiantes/<id>: Eliminar
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    e = Estudiante.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"mensaje": f"Estudiante con ID {id} eliminado"})

# GET /estudiantes/buscar: Búsqueda insensible a mayúsculas
@app.route('/estudiantes/buscar', methods=['GET'])
def buscar_estudiantes():
    nom = request.args.get('nombre', '')
    ape = request.args.get('apellido', '')
    
    query = Estudiante.query.filter(
        Estudiante.nombre.ilike(f"%{nom}%"),
        Estudiante.apellido.ilike(f"%{ape}%")
    ).all()
    
    return jsonify([{"nombre": e.nombre, "apellido": e.apellido, "nota": e.nota} for e in query])

# GET /estudiantes/filtrar: Solo aprobados
@app.route('/estudiantes/filtrar', methods=['GET'])
def filtrar_aprobados():
    aprobados = Estudiante.query.filter_by(aprobado=True).all()
    return jsonify([{"nombre": a.nombre, "apellido": a.apellido, "nota": a.nota} for a in aprobados])

if __name__ == '__main__':
    app.run(debug=True)