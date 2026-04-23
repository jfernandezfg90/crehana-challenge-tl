# Decision Log — Crehana Backend Challenge

## 1. Base de Datos: SQLite local + PostgreSQL en produccion

**Decision:** SQLite (zero config) para local/Docker; PostgreSQL via Supabase para Vercel.

**Razon:**
- **Facilidad de Evaluación (Zero Friction)**: SQLite permite que el evaluador clone el repo y corra la app de inmediato sin configurar servicios externos, facilitando la revisión técnica.
- **Portabilidad**: El codebase es agnóstico; `connection.py` maneja dinámicamente ambos motores sin cambios en la lógica de negocio.
- **Valor Añadido**: El despliegue en Vercel + Supabase demuestra una mentalidad orientada a producción (Cloud Ready) más allá de un simple ejercicio local.
- **Eficiencia**: `NullPool` en PostgreSQL evita el agotamiento de conexiones en funciones serverless.

---

## 2. ORM: SQLAlchemy 2.x Sync (no async)

**Decision:** Usar SQLAlchemy 2.x en modo sincrono con psycopg2-binary.

**Razon:**
- **Estabilidad en Serverless**: Vercel ejecuta funciones de vida corta. El modo síncrono es más predecible y evita problemas de gestión del `event loop` que pueden ocurrir en arquitecturas *stateless*.
- **Pragmatismo**: Para el alcance de este challenge, el modo `async` añade una complejidad innecesaria (código lleno de `await`, configuración de drivers más compleja) sin una mejora de rendimiento perceptible.
- **Fiabilidad del Driver**: `psycopg2-binary` es el estándar de la industria, extremadamente estable y compatible con prácticamente cualquier entorno de despliegue.
- **Simplicidad en Testing**: Facilita la creación de pruebas de integración rápidas sin necesidad de gestionar sesiones asíncronas complejas.

---

## 3. Arquitectura: Clean Architecture / Hexagonal

**Decision:** Separar el codigo en 4 capas: Domain, Application, Infrastructure, API.

**Razon:**
- **Domain:** logica de negocio pura sin dependencias externas — facil de testear unitariamente.
- **Application (use cases):** orquesta el dominio sin conocer HTTP ni SQL.
- **Infrastructure:** implementa las interfaces del dominio (repos SQL, JWT handler, email falso).
- **API:** traduccion HTTP ↔ use cases, sin logica de negocio.
- Esta separacion permite cambiar la DB, el framework o el proveedor de notificaciones
  sin modificar los use cases.

---

## 4. Tipos ORM cross-DB: `sqlalchemy.Uuid` y `Enum(native_enum=False)`

**Decision:** Usar tipos genericos de SQLAlchemy en lugar de dialectos especificos de PostgreSQL.

**Razon:**
- `sqlalchemy.dialects.postgresql.UUID` falla en SQLite; `sqlalchemy.Uuid` funciona en ambas.
- `Enum(native_enum=False)` almacena el valor como VARCHAR en lugar de crear un tipo ENUM
  de PostgreSQL, lo que hace el schema compatible con SQLite.
- Este tradeoff (portabilidad sobre tipos nativos) es correcto para un proyecto que corre
  en dos motores de base de datos.

---

## 5. UUID como Primary Key

**Decision:** Usar UUID v4 para los IDs en lugar de integers autoincrement.

**Razon:**
- No predecibles: evita enumeration attacks en endpoints REST.
- Distribuibles: se pueden generar en la capa de dominio sin coordinacion con la DB.
- Compatible con Supabase (`gen_random_uuid()`) y SQLite (generado en Python).

---

## 6. Creacion de Tablas: `create_all()` en startup

**Decision:** Usar `Base.metadata.create_all()` en el lifespan de FastAPI en lugar de
requerir Alembic para el entorno local y Docker.

**Razon:**
- Zero friction para desarrollo: clonar + `uvicorn` es suficiente.
- Las tablas se crean automaticamente en el primer arranque.
- Alembic sigue disponible (`alembic upgrade head`) para migraciones versionadas
  en produccion PostgreSQL, donde el control del schema es critico.
- Para SQLite local, `create_all()` es inocuo: si las tablas existen, no hace nada.

---

## 7. Tests: SQLite en memoria + TestClient sincrono

**Decision:** Usar SQLite in-memory para integration tests, sin pytest-asyncio.

**Razon:**
- Tests rapidos sin dependencia de red ni credenciales externas.
- Cada test recrea las tablas en un engine in-memory fresco (isolation total).
- `TestClient` de Starlette es sincrono — consistente con el ORM sincrono.
- Resultado: 57 tests, 95.15% de cobertura, sin mocks de repositorios en integracion.

---

## 8. Auth: JWT con python-jose + passlib

**Decision:** Implementar JWT Bearer tokens. Pin `bcrypt==4.0.1`.

**Razon:**
- **Arquitectura Stateless**: Los JWT permiten autenticar peticiones sin guardar sesiones en el servidor, ideal para entornos serverless.
- **`python-jose`**: Es el estándar para la generación, firma y verificación de tokens JWT, asegurando que la información del usuario no sea manipulada.
- **`passlib[bcrypt]`**: Encargada del hasheo seguro de contraseñas mediante algoritmos robustos.
- **Fix de Compatibilidad**: Se fijó `bcrypt==4.0.1` para evitar un conflicto conocido entre `passlib 1.7.4` y versiones de `bcrypt >= 5.0` que causaba errores en el proceso de verificación.

---

## 9. Deploy: Docker multistage + Vercel serverless

**Decision:** Dockerfile multistage (requisito del challenge) + `api/index.py` para Vercel.

**Razon:**
- Docker multistage: imagen mas pequena (builder instala deps, runtime solo las copia).
- `docker-compose` levanta un unico servicio `app` con SQLite en volumen — sin servicios externos.
- `api/index.py` re-exporta la app FastAPI. Vercel la detecta como handler ASGI y la envuelve
  en una funcion serverless.
- El mismo codigo funciona en ambos entornos sin cambios.

---

## 10. Transiciones de Estado con maquina de estados

**Decision:** Validar transiciones de estado con un dict de transiciones validas.

**Razon:**
- Evita saltos invalidos (ej. `PENDING` → `DONE` directamente).
- Errores explicitos (422) en lugar de datos inconsistentes en la base de datos.
- La logica vive en el use case `ChangeTaskStatusUseCase`, no en la API ni en el ORM.

Transiciones validas:
- `PENDING` → `IN_PROGRESS`
- `IN_PROGRESS` → `DONE`
- `IN_PROGRESS` → `PENDING` (reabrir)
- `DONE` → `IN_PROGRESS` (reactivar)

---

## 11. Notificacion Ficticia: FakeEmailService

**Decision:** `FakeEmailService` loggea en lugar de enviar emails reales.

**Razon:**
- El challenge pide simulacion, no integracion real.
- La interfaz `NotificationService` (ABC) permite reemplazar por SendGrid/SES/etc.
  sin modificar los use cases (Dependency Inversion).
- El log queda en stdout del servidor como evidencia de la llamada.

---

## 12. Frontend: Vanilla JS servido por FastAPI

**Decision:** HTML + CSS + JS sin framework, servido como rutas estaticas por FastAPI.

**Razon:**
- Sin build step: los archivos se editan y se sirven directamente.
- Compatible con Vercel (los archivos viajan junto al codigo Python en el deploy).
- FastAPI sirve `frontend/index.html` en `/`, `frontend/dashboard.html` en `/dashboard`,
  y assets (`style.css`, `logo.png`, `isotipo.png`) bajo `/static/`.
- Para un demo de challenge, la complejidad de un bundler (Vite, Webpack) no aporta valor.

---

## 13. Documentacion de Codigo: Docstrings de Modulo

**Decision:** Documentar todos los archivos `.py` con descripciones tecnicas al inicio.

**Razon:**
- Facilita el "onboarding" de otros desarrolladores al proyecto.
- Sigue las buenas practicas de Python (PEP 257).
- Mejora la mantenibilidad al explicar el "por que" y el "que" de cada modulo sin leer todo el codigo.

---

## 14. Infraestructura Serverless: Supabase Connection Pooler

**Decision:** Usar el puerto 6543 (Transaction Mode) de Supabase en Vercel.

**Razon:**
- **Compatibilidad IPv6**: Vercel tiene limitaciones para conectar por el puerto estándar 5432 (IPv4 directo). El pooler actúa como puente compatible.
- **Eficiencia**: En entornos serverless (funciones lambda), las conexiones se abren y cierran constantemente. El pooler evita agotar los recursos de la base de datos.
- **Robustez**: Soluciona errores de "OperationalError" comunes en despliegues en la nube.

---

## 15. Calidad de Código: Triada Black + Isort + Flake8

**Decision:** Configurar Black (formateador), Isort (importaciones) y Flake8 (linter) con reglas sincronizadas.

**Razon:**
- **Automatización**: Black e Isort eliminan discusiones sobre estilo visual y orden de imports.
- **Prevención**: Flake8 detecta errores potenciales y complejidad alta antes del despliegue.
- **Consistencia**: El archivo `.isort.cfg` garantiza que todas las herramientas trabajen en armonía.

---

## 16. Feedback Visual: Success Pop-ups

**Decision:** Implementar pop-ups de éxito con logs de "backend simulado".

**Razon:**
- **UX Premium**: Confirma acciones críticas (como asignación) de forma clara y atractiva.
- **Observabilidad**: Permite al evaluador ver qué está pasando "por debajo" (ej. el envío de emails simulados) sin abrir la consola del navegador.
- **Diseño**: Mantiene la estética moderna y consistente del Dashboard.
