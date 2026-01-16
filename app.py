import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    aprobado = db.Column(db.Boolean, default=False)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)

def cargar_datos_iniciales():
    if Estudiante.query.count() == 0:
        if os.path.exists('estudiante.json'):
            with open('estudiante.json', 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
                for item in datos_json:
                    f_str = item['fecha']['$date'].replace('Z', '')
                    f_dt = datetime.fromisoformat(f_str)
                    val_nota = float(item['nota'])
                    nuevo = Estudiante(
                        nombre=item['nombre'],
                        apellido=item['apellido'],
                        aprobado=(val_nota > 5.0),
                        nota=val_nota,
                        fecha=f_dt
                    )
                    db.session.add(nuevo)
            db.session.commit()

with app.app_context():
    db.create_all()
    cargar_datos_iniciales()

@app.route('/')
def index():
    todos = Estudiante.query.all()
    return render_template('index.html', estudiantes=todos)

@app.route('/web/estudiante/<int:id>')
def web_ver_uno(id):
    e = Estudiante.query.get_or_404(id)
    return render_template('index.html', estudiantes=[e], modo_detalle=True)

@app.route('/web/crear', methods=['POST'])
def web_crear():
    n = request.form.get('nombre')
    a = request.form.get('apellido')
    nt = float(request.form.get('nota'))
    nt = max(0.0, min(10.0, nt))
    fecha_fija = datetime(2026, 1, 15)
    nuevo = Estudiante(nombre=n, apellido=a, nota=nt, aprobado=(nt > 5.0), fecha=fecha_fija)
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/web/editar/<int:id>')
def web_editar_form(id):
    e = Estudiante.query.get_or_404(id)
    todos = Estudiante.query.all()
    return render_template('index.html', estudiantes=todos, estudiante_editar=e)

@app.route('/web/actualizar/<int:id>', methods=['POST'])
def web_actualizar(id):
    e = Estudiante.query.get_or_404(id)
    e.nombre = request.form.get('nombre')
    e.apellido = request.form.get('apellido')
    nt = float(request.form.get('nota'))
    e.nota = max(0.0, min(10.0, nt))
    e.aprobado = (e.nota > 5.0)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/web/eliminar/<int:id>')
def web_eliminar(id):
    e = Estudiante.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('index'))

# --- RUTA DE BÚSQUEDA CORREGIDA PARA NOMBRES COMPLETOS ---
@app.route('/web/buscar')
def web_buscar():
    q = request.args.get('q', '').strip()
    # Filtro inteligente: Busca en nombre, en apellido, o en la combinación de ambos
    res = Estudiante.query.filter(
        (Estudiante.nombre.ilike(f"%{q}%")) | 
        (Estudiante.apellido.ilike(f"%{q}%")) |
        ((Estudiante.nombre + " " + Estudiante.apellido).ilike(f"%{q}%"))
    ).all()
    return render_template('index.html', estudiantes=res)

@app.route('/web/filtrar')
def web_filtrar():
    aprobados = Estudiante.query.filter_by(aprobado=True).all()
    return render_template('index.html', estudiantes=aprobados)

if __name__ == '__main__':
    app.run(debug=True)