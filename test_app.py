import pytest
import sqlite3
from app import app, init_db, DB_NAME

# Fixture: Prepara un entorno limpio antes de CADA prueba
@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # Limpiamos la base de datos para que las pruebas no se contaminen entre sí
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM tareas")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

# ==========================================
# PRUEBAS DE ÉXITO (Happy Paths)
# ==========================================

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 202
    assert response.json['status'] == "ok"

def test_crear_tarea(client):
    response = client.post('/api/tareas', json={"titulo": "Aprender CI/CD", "completada": False})
    assert response.status_code == 201
    assert response.json['data']['titulo'] == "Aprender CI/CD"

def test_listar_tareas(client):
    # Insertamos una primero
    client.post('/api/tareas', json={"titulo": "Tarea 1"})
    response = client.get('/api/tareas')
    assert response.status_code == 200
    assert len(response.json['data']) == 1

def test_obtener_tarea_individual(client):
    post_res = client.post('/api/tareas', json={"titulo": "Tarea Específica"})
    tarea_id = post_res.json['data']['id']
    
    response = client.get(f'/api/tareas/{tarea_id}')
    assert response.status_code == 200
    assert response.json['data']['titulo'] == "Tarea Específica"

def test_actualizar_tarea(client):
    post_res = client.post('/api/tareas', json={"titulo": "Tarea Vieja"})
    tarea_id = post_res.json['data']['id']
    
    response = client.put(f'/api/tareas/{tarea_id}', json={"titulo": "Tarea Nueva", "completada": True})
    assert response.status_code == 200
    assert response.json['data']['titulo'] == "Tarea Nueva"
    assert response.json['data']['completada'] == True

def test_eliminar_tarea(client):
    post_res = client.post('/api/tareas', json={"titulo": "Tarea a borrar"})
    tarea_id = post_res.json['data']['id']
    
    response = client.delete(f'/api/tareas/{tarea_id}')
    assert response.status_code == 200
    
    # Verificamos que realmente se borró
    check_res = client.get(f'/api/tareas/{tarea_id}')
    assert check_res.status_code == 404

# ==========================================
# PRUEBAS DE FALLO (Errores de Usuario)
# ==========================================

def test_crear_tarea_sin_titulo(client):
    response = client.post('/api/tareas', json={"completada": False}) # Falta 'titulo'
    assert response.status_code == 400

def test_obtener_tarea_inexistente(client):
    response = client.get('/api/tareas/999')
    assert response.status_code == 404

def test_actualizar_tarea_inexistente(client):
    response = client.put('/api/tareas/999', json={"titulo": "Fantasma"})
    assert response.status_code == 404

def test_actualizar_tarea_sin_datos(client):
    post_res = client.post('/api/tareas', json={"titulo": "Tarea"})
    tarea_id = post_res.json['data']['id']
    
    response = client.put(f'/api/tareas/{tarea_id}', json={}) # Mandamos un JSON vacío
    assert response.status_code == 400

def test_eliminar_tarea_inexistente(client):
    response = client.delete('/api/tareas/999')
    assert response.status_code == 404