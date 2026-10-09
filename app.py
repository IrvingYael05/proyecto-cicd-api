from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "tareas.db"

# Inicializar Base de Datos SQLite
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            titulo TEXT NOT NULL, 
            completada INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# LOS 6 ENDPOINTS
# ==========================================

# 1. GET /api/health - Comprobación de salud
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok-revisando-uteq", "message": "API funcionando correctamente"}), 202

# 2. GET /api/tareas - Listar todas las tareas
@app.route('/api/tareas', methods=['GET'])
def get_tareas():
    conn = get_db()
    tareas = [dict(row) for row in conn.execute("SELECT * FROM tareas").fetchall()]
    return jsonify({"data": tareas}), 200

# 3. GET /api/tareas/<id> - Obtener una tarea específica
@app.route('/api/tareas/<int:id>', methods=['GET'])
def get_tarea(id):
    conn = get_db()
    tarea = conn.execute("SELECT * FROM tareas WHERE id = ?", (id,)).fetchone()
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify({"data": dict(tarea)}), 200

# 4. POST /api/tareas - Crear una nueva tarea
@app.route('/api/tareas', methods=['POST'])
def create_tarea():
    if not request.json or 'titulo' not in request.json:
        return jsonify({"error": "Falta el título de la tarea"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    completada = 1 if request.json.get('completada', False) else 0
    cursor.execute("INSERT INTO tareas (titulo, completada) VALUES (?, ?)", (request.json['titulo'], completada))
    conn.commit()
    
    nueva_tarea = {
        "id": cursor.lastrowid,
        "titulo": request.json['titulo'],
        "completada": bool(completada)
    }
    return jsonify({"data": nueva_tarea}), 201

# 5. PUT /api/tareas/<id> - Actualizar una tarea
@app.route('/api/tareas/<int:id>', methods=['PUT'])
def update_tarea(id):
    conn = get_db()
    tarea = conn.execute("SELECT * FROM tareas WHERE id = ?", (id,)).fetchone()
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    if not request.json:
        return jsonify({"error": "Datos inválidos"}), 400

    nuevo_titulo = request.json.get('titulo', tarea['titulo'])
    # Convertimos el booleano a entero (0 o 1) para SQLite
    nueva_completada = 1 if request.json.get('completada', bool(tarea['completada'])) else 0

    conn.execute("UPDATE tareas SET titulo = ?, completada = ? WHERE id = ?", (nuevo_titulo, nueva_completada, id))
    conn.commit()
    
    tarea_actualizada = {"id": id, "titulo": nuevo_titulo, "completada": bool(nueva_completada)}
    return jsonify({"data": tarea_actualizada}), 200

# 6. DELETE /api/tareas/<id> - Eliminar una tarea
@app.route('/api/tareas/<int:id>', methods=['DELETE'])
def delete_tarea(id):
    conn = get_db()
    tarea = conn.execute("SELECT * FROM tareas WHERE id = ?", (id,)).fetchone()
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    conn.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conn.commit()
    return jsonify({"message": "Tarea eliminada exitosamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)