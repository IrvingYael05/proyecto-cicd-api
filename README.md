# Proyecto Integrador: Pipeline CI/CD Automatizado para API REST  
  
Este repositorio contiene la implementación de una API REST desarrollada en Python (Flask) con una arquitectura de despliegue y entrega continua (CI/CD) completamente automatizada. El proyecto utiliza GitHub Actions para la validación de código, empaquetado en Docker y despliegue ininterrumpido en un servidor Amazon EC2.  
  
## Arquitectura y Tecnologías  
  
El ecosistema del proyecto está compuesto por las siguientes herramientas:  
  
*   **Backend:** Python 3.12 con el micro-framework **Flask**.  
*   **Base de Datos:** **SQLite** (Integrada) para la persistencia de datos (Gestión de Tareas).  
*   **Testing y QA:** **Pytest** y `pytest-cov` para pruebas automatizadas y medición de cobertura de código (Code Coverage > 70%).  
*   **Contenerización:** **Docker** para empaquetar la aplicación en una imagen ligera e inmutable, gestionada en **Docker Hub**.  
*   **Orquestación CI/CD:** **GitHub Actions** para automatizar el flujo de trabajo en cada `push` a la rama `main`.  
*   **Infraestructura en la Nube:** **AWS EC2** (Ubuntu Server) para el alojamiento web de producción, operando en el puerto 80.  
  
---  
  
## Comandos Locales (Entorno de Desarrollo)  
  
Para ejecutar, probar o modificar este proyecto en tu computadora local, sigue estos pasos:  
  
### 1. Clonar el repositorio e instalar dependencias  
```bash  
git clone https://github.com/IrvingYael05/proyecto-cicd-api.git  
cd proyecto-cicd  
pip install -r requirements.txt
```

### 2. Ejecutar la API localmente
``` bash
python app.py  
```

*La API estará disponible en `*http://localhost:80*` (o `*http://127.0.0.1:80*`).*

### 3. Ejecutar pruebas unitarias y cobertura de código

Para verificar que el código cumple con el estándar de calidad y supera el 70% de cobertura, ejecuta:

``` bash
python -m pytest --cov=app --cov-report=term-missing  
```

### 4. Construir y probar la imagen Docker localmente
``` bash
# Construir la imagen  
docker build -t api-tareas:latest .  
  
# Ejecutar el contenedor en el puerto 8080 local mapeado al 80 del contenedor  
docker run -d -p 8080:80 --name test-api api-tareas:latest  
```

## Pasos de Configuración (Pipeline CI/CD)

El archivo de configuración principal se encuentra en `.github/workflows/main.yml`. Este pipeline orquesta dos fases:

1.  **Integración Continua (CI):** Levanta un entorno de pruebas, instala dependencias, ejecuta `pytest` verificando que la cobertura no baje del 70% (`--cov-fail-under=70`), construye la imagen Docker y la sube a Docker Hub etiquetada con la versión `latest` y el hash del commit actual.
2.  **Despliegue Continuo (CD):** Si las pruebas pasan, se conecta al servidor AWS EC2 mediante SSH, descarga la imagen actualizada y reinicia el servicio sin tiempos de caída.

### Secretos de GitHub Requeridos

Para que la automatización funcione por seguridad, este repositorio requiere configurar las siguientes variables en la sección **Settings > Secrets and variables > Actions**:

-   `DOCKER_USERNAME`: Usuario de Docker Hub.
-   `DOCKER_PASSWORD`: Personal Access Token (PAT) de Docker Hub con permisos de lectura/escritura.
-   `EC2_HOST`: Dirección IP pública de la instancia AWS EC2.
-   `EC2_USER`: Usuario del servidor remoto (ej. `ubuntu`).
-   `EC2_SSH_KEY`: Clave privada RSA (`.pem`) generada por AWS para autenticación.

## Endpoints Disponibles

La API expone los siguientes 6 endpoints principales en formato JSON:

-   `GET /api/health` - Verifica el estado de salud del servidor.
-   `GET /api/tareas` - Lista todas las tareas registradas.
-   `GET /api/tareas/<id>` - Muestra los detalles de una tarea específica.
-   `POST /api/tareas` - Crea una nueva tarea (requiere `titulo` en el body).
-   `PUT /api/tareas/<id>` - Actualiza una tarea existente.
-   `DELETE /api/tareas/<id>` - Elimina una tarea de la base de datos.