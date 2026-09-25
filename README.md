# Sistema de Gestión de Donaciones

API académica para gestionar usuarios y donantes de alimentos y recursos entre empresas y organizaciones sociales. El alcance está limitado al módulo documentado: autenticación JWT, autorización por roles y CRUD de donantes. No incluye frontend.

## Objetivos

* Proteger credenciales con Argon2 y solicitudes con JWT expirables.
* Aplicar los roles `admin` y `user` en el backend.
* Mantener cobertura automatizada mínima de 80 %.
* Preparar CI/CD, Docker, SonarQube/SonarCloud y OWASP ZAP.

## Tecnologías y arquitectura

FastAPI expone la API y OpenAPI; Pydantic valida entradas; SQLAlchemy abstrae SQLite; Argon2 protege contraseñas; PyJWT firma tokens; Pytest valida comportamiento. La separación principal es `routers` para HTTP, `schemas` para contratos, `models` para persistencia, `security` para criptografía y `dependencies` para autorización.

## Estructura

```text
app/                 API y dominio
tests/               pruebas aisladas con SQLite en memoria
scripts/              creación de admin y escaneo ZAP
reports/              evidencias de Pytest, ZAP y Sonar
.github/workflows/    pipeline CI/CD
```

## Requisitos

* Python 3.12+
* Docker para construir/ejecutar la imagen
* Git para control de versiones
* Cuenta GitHub y, opcionalmente, SonarCloud y Render para servicios externos

## Instalación local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

En Linux/macOS usa `source .venv/bin/activate` y `cp .env.example .env`.

## Variables de entorno

`DATABASE_URL` define la conexión, `JWT_SECRET_KEY` firma tokens, `JWT_ALGORITHM` define el algoritmo y `ACCESS_TOKEN_EXPIRE_MINUTES` fija la expiración. En producción usa un secreto aleatorio largo y nunca subas `.env`.

## Ejecución local

```powershell
uvicorn app.main:app --reload
```

La documentación está en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), el esquema en `/openapi.json` y la comprobación básica en `/health`.

## Administrador de demostración

El registro público fuerza el rol `user`. Para crear un administrador de forma controlada:

```powershell
$env:ADMIN_NAME="Administrador Académico"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="CambiaEstaClave1!"
python scripts/create_admin.py
```

El script crea o actualiza únicamente ese administrador usando el mismo `DATABASE_URL` de la API. En Linux/macOS exporta las tres variables antes del comando.

## Endpoints y roles

| Método | Endpoint | Acceso |
|---|---|---|
| POST | `/auth/register` | Público, siempre crea `user` |
| POST | `/auth/login` | Público, devuelve JWT |
| GET | `/auth/me` | JWT |
| POST | `/donantes` | `user`, `admin` |
| GET | `/donantes` | `admin` |
| GET | `/donantes/{id}` | `user`, `admin` |
| PUT | `/donantes/{id}` | `admin` |
| DELETE | `/donantes/{id}` | `admin` |

En Swagger usa el token como `Bearer <token>`. Un usuario normal que intente listar, actualizar o eliminar recibirá `403 Forbidden`.

## Pruebas y cobertura

```powershell
pytest --cov=app --cov-report=term-missing --cov-report=html:reports/pytest/htmlcov --cov-report=xml:reports/pytest/coverage.xml --cov-fail-under=80
```

Las pruebas usan una base SQLite aislada en memoria. Los resultados reales se registran en `RESULTADOS_PARA_INFORME.md` después de cada ejecución.

## Docker

```powershell
docker build -t sistema-donaciones .
docker run --rm -p 8000:8000 -e JWT_SECRET_KEY="secreto-local-largo" sistema-donaciones
```

Para persistir la base de datos local, agrega `-v ${PWD}/data:/app/data` y usa `DATABASE_URL=sqlite:///./data/donaciones.db`.

## GitHub Actions

`.github/workflows/ci-cd.yml` ejecuta pruebas con umbral de 80 %, guarda el artifact de cobertura y construye Docker. El job de calidad se activa en push cuando existen `SONAR_TOKEN` y `SONAR_HOST_URL`; el despliegue se activa en push a `main` cuando existe `RENDER_DEPLOY_HOOK_URL`.

## SonarQube/SonarCloud

El archivo `sonar-project.properties` apunta a `reports/pytest/coverage.xml`. Para SonarCloud configura `SONAR_TOKEN` y `SONAR_HOST_URL` como secretos de GitHub y ajusta `sonar.projectKey`/organización según tu cuenta. Para SonarQube local, ejecuta `sonar-scanner` después de Pytest con cobertura. No se incluyen métricas hasta realizar un análisis real.

## OWASP ZAP

Con la API ejecutándose y Docker disponible:

```bash
bash scripts/run_zap.sh http://localhost:8000
```

En PowerShell puedes usar `.scriptsun_zap.ps1 http://host.docker.internal:8000`.

El script usa ZAP API Scan contra `/openapi.json` y guarda `reports/zap/zap-report.html` y `reports/zap/zap-report.json`. Revisa alertas, corrige lo procedente y vuelve a ejecutar el escaneo antes de completar el informe.

## Staging y despliegue

La integración preparada usa Render Deploy Hook. Crea un Web Service desde el repositorio, define el comando `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, agrega `DATABASE_URL` y `JWT_SECRET_KEY` en el entorno de Render, copia el Deploy Hook y guárdalo en GitHub como `RENDER_DEPLOY_HOOK_URL`. Después de un push a `main`, verifica la URL `/health`, `/docs` y los logs del servicio. No se reporta una URL hasta realizar estos pasos.

## Evidencias y limitaciones

`RESULTADOS_PARA_INFORME.md` enumera exactamente las capturas requeridas y distingue resultados reales de tareas pendientes. Sonar, ZAP, GitHub Actions y Render requieren ejecución externa, acceso a servicios o credenciales; el repositorio deja la configuración lista sin inventar sus resultados.
