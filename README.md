# Crehana Task Manager

API REST para gestionar listas de tareas y tareas, desarrollada como desafio tecnico backend para Crehana. Incluye un frontend demo servido por la propia API.

## Tech Stack

- **Python 3.11** + **FastAPI**
- **SQLite** (local/Docker, zero config) / **PostgreSQL via Supabase** (produccion/Vercel)
- **SQLAlchemy 2.x** sync — compatible con ambas bases de datos
- **JWT** (python-jose + passlib/bcrypt)
- **pytest** — 57 tests, 95%+ cobertura
- **Docker** multistage + **Vercel** serverless

## Arquitectura

El proyecto implementa **Clean Architecture (Arquitectura Hexagonal)** para garantizar el desacoplamiento total de la lógica de negocio y la infraestructura.

```text
app/
├── domain/          # Capa de Corazón: Entidades puras y reglas de negocio.
├── application/     # Capa de Orquestación: Casos de uso (Application Services).
├── infrastructure/  # Capa de Adaptadores: Detalles técnicos (SQL, JWT, Email).
└── api/             # Capa de Entrada: Interfaz HTTP (FastAPI, Schemas).
```

### Responsabilidades por Capa:

*   **Domain**: Contiene las entidades (`Task`, `User`), objetos de valor (`Status`), excepciones de negocio e **interfaces de repositorios**. Es 100% independiente de cualquier framework o librería externa.
*   **Application**: Implementa los **Casos de Uso** (ej: `CreateTask`, `AssignTask`). Orquesta el flujo de datos usando las interfaces del dominio, sin saber si los datos vienen de SQL o una API externa.
*   **Infrastructure**: Contiene las implementaciones técnicas. Aquí reside la configuración de **SQLAlchemy**, los repositorios SQL concretos, el manejo de JWT y el servicio de notificaciones simulado.
*   **API**: Define la interfaz externa. Maneja las peticiones HTTP, la validación de entrada con **Pydantic**, la inyección de dependencias y la gestión de errores globales.

> [!TIP]
> Esta estructura permite que, por ejemplo, podamos cambiar la base de datos de SQLite a PostgreSQL o el proveedor de email sin modificar ni una sola línea de código en la lógica de negocio (`domain` y `application`).

## Setup Local (SQLite, zero config)

```bash
# 1. Clonar
git clone https://github.com/jfernandezfg90/crehana-challenge-tl.git
cd crehana-challenge-tl

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Dependencias
pip install -r requirements-dev.txt

# 4. Arrancar — las tablas se crean automaticamente al iniciar
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Frontend: http://localhost:8000

No se necesita archivo `.env` para desarrollo local. Para personalizar:

```bash
cp .env.example .env
# editar .env con tus valores
```

## Ejecucion con Docker

> [!NOTE]
> Requiere tener **Docker Desktop** (o Docker Engine) instalado y en ejecución.

```bash
docker-compose up --build
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Frontend: http://localhost:8000

El contenedor usa SQLite persistente en un volumen Docker (`db_data`).
No requiere base de datos externa.

## Ejecucion de Pruebas

```bash
# Todos los tests con cobertura
pytest

# Por categoria
pytest tests/unit/
pytest tests/integration/

# Reporte HTML de cobertura
pytest --cov=app --cov-report=html
start htmlcov/index.html    # En Windows
open htmlcov/index.html     # En macOS
```

## Linting

Se utilizan las siguientes herramientas para garantizar la calidad y consistencia del código:

- **flake8**: Analizador estático (linter) para encontrar errores y asegurar cumplimiento de PEP 8.
- **black**: Formateador de código automático que garantiza un estilo visual consistente.
- **isort**: Herramienta para organizar las importaciones alfabéticamente y por secciones.

```bash
flake8 app tests              # Analizar calidad del código
black --check app tests       # Verificar si el formato es correcto
isort --check-only app tests  # Verificar el orden de las importaciones
```

## Deploy en Vercel (produccion con PostgreSQL)

Vercel requiere una base de datos externa. Se recomienda **Supabase** (PostgreSQL gratuito).

### Pasos críticos para la conexión:

1.  **Obtener la URI del Pooler**: En Supabase, ve a *Connect > ORMs* y copia la URI del **Connection Pooler** (Puerto `6543`).
2.  **Codificar Contraseña**: Si tu contraseña tiene caracteres especiales (como `@`), cámbialos por su equivalente URL (ej: `@` -> `%40`).
3.  **Configurar Variables en Vercel**:
    *   `DATABASE_URL`: `postgresql://postgres.[ID]:[PASS]%40@[HOST]:6543/postgres`
    *   `SECRET_KEY`: Una clave aleatoria para JWT.

```bash
# 1. Instalar CLI
npm i -g vercel

# 2. Desplegar (Sigue los pasos para linkear el repo)
vercel deploy

# 3. Pasar a producción
vercel --prod
```

- API: https://crehana-challenge-tl.vercel.app
- Docs: https://crehana-challenge-tl.vercel.app/docs
- Frontend: https://crehana-challenge-tl.vercel.app

> [!IMPORTANTE]
> Se recomienda usar el puerto **6543** (Transaction Mode) de Supabase para evitar errores de conexión IPv6 en entornos Serverless como Vercel.

En produccion, las tablas se crean automaticamente en el primer request gracias al lifespan de FastAPI.
Alembic esta disponible si se necesitan migraciones versionadas contra PostgreSQL:

```bash
DATABASE_URL=postgresql://... alembic upgrade head
```

## Frontend

El dashboard esta integrado en la misma API y se sirve como archivos estaticos:

| Ruta | Descripcion |
|------|-------------|
| `/` | Login / Registro |
| `/dashboard` | Panel de tareas |

Tecnologias: HTML + CSS + Vanilla JS, sin build step. Activos graficos en `assets/`.

## Endpoints API

### Auth

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Registrar usuario |
| POST | `/api/v1/auth/login` | Login → JWT token |

### Task Lists _(requieren JWT)_

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/api/v1/task-lists` | Crear lista |
| GET | `/api/v1/task-lists` | Listar mis listas |
| GET | `/api/v1/task-lists/{id}` | Obtener una lista |
| PUT | `/api/v1/task-lists/{id}` | Actualizar lista |
| DELETE | `/api/v1/task-lists/{id}` | Eliminar lista |

### Tasks _(requieren JWT)_

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/api/v1/task-lists/{list_id}/tasks` | Crear tarea |
| GET | `/api/v1/task-lists/{list_id}/tasks` | Listar tareas (filtros + % completitud) |
| GET | `/api/v1/task-lists/{list_id}/tasks/{task_id}` | Obtener tarea |
| PUT | `/api/v1/task-lists/{list_id}/tasks/{task_id}` | Actualizar tarea |
| DELETE | `/api/v1/task-lists/{list_id}/tasks/{task_id}` | Eliminar tarea |
| PATCH | `/api/v1/task-lists/{list_id}/tasks/{task_id}/status` | Cambiar estado |
| PATCH | `/api/v1/task-lists/{list_id}/tasks/{task_id}/assign` | Asignar usuario |

### Filtros y respuesta de listado de tareas

```
GET /api/v1/task-lists/{list_id}/tasks?status=DONE&priority=HIGH
```

```json
{
  "tasks": [...],
  "total": 5,
  "completion_percentage": 40.0
}
```

## Estados de Tarea

```
PENDING → IN_PROGRESS → DONE
           ↑____________↓
```

Transiciones validas:
- `PENDING` → `IN_PROGRESS`
- `IN_PROGRESS` → `DONE`
- `IN_PROGRESS` → `PENDING` (reabrir)
- `DONE` → `IN_PROGRESS` (reactivar)

Cualquier otra transicion retorna `422 Unprocessable Entity`.

## Documentacion de Codigo

Todos los archivos `.py` del proyecto han sido documentados con **docstrings de modulo** que explican su responsabilidad dentro de la arquitectura. Esto facilita la navegacion y el mantenimiento del codigo siguiendo estandares profesionales de Python (PEP 257).

## Frontend y Experiencia de Usuario (UI/UX)

El dashboard ha sido diseñado para ser funcional y visualmente atractivo. 

- **Feedback Visual**: Al asignar una tarea a un usuario, se muestra un **Pop-up de exito** premium que incluye:
    - Confirmacion visual con icono ✅.
    - Nombre del usuario asignado.
    - Un log simulado que replica el mensaje de notificacion del backend: `[EMAIL SIMULADO] Notificacion de asignacion enviada a '...' para la tarea '...'`.
- **Estados y Transiciones**: El sistema guia al usuario permitiendo solo transiciones logicas de estado, deshabilitando botones cuando no hay una accion valida siguiente.

## Mantenimiento y Limpieza

- **`htmlcov/`**: Esta carpeta contiene el reporte visual de cobertura de tests. Es un artefacto generado y puede ser eliminado con seguridad; se regenera al correr `pytest --cov`.
- **`alembic/`**: Contiene las migraciones de la base de datos. Es vital para evolucionar el esquema de la base de datos en entornos de produccion (PostgreSQL) sin perdida de datos.
- **`.flake8`**: Configuracion para el linter, asegurando que el estilo del codigo se mantenga consistente y compatible con formateadores como Black.

## Licencia

Este proyecto fue desarrollado como prueba técnica y es de libre uso para fines educativos.
