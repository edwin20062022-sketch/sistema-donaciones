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

La ejecución local verificada el 24 de septiembre de 2026 completó 12 de 12 pruebas y obtuvo 97.36 % de cobertura global.

## Docker

En Windows utiliza Docker Desktop con el backend WSL 2 y contenedores Linux.

```powershell
docker desktop start
docker desktop engine use linux
docker build -t sistema-donaciones:latest .
docker run --rm -p 8000:8000 -e JWT_SECRET_KEY="secreto-local-largo" sistema-donaciones:latest
docker ps
docker logs <container_id_o_nombre>
```

Verifica la aplicación en [http://localhost:8000/docs](http://localhost:8000/docs) y [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json). Para persistir la base de datos local, agrega `-v ${PWD}/data:/app/data` y usa `DATABASE_URL=sqlite:///./data/donaciones.db`.

## GitHub Actions

El repositorio está publicado en [GitHub](https://github.com/edwin20062022-sketch/sistema-donaciones). `.github/workflows/ci-cd.yml` ejecuta pruebas con umbral de 80 %, guarda el artifact de cobertura y construye Docker. El job de calidad se activa en push cuando existen `SONAR_TOKEN` y `SONAR_HOST_URL`; el despliegue se activa en push a `main` cuando existe `RENDER_DEPLOY_HOOK_URL`.

La primera ejecución verificada de [CI/CD](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36094031338) finalizó correctamente: pruebas y cobertura, build de Docker y análisis de calidad completaron. El escaneo externo de Sonar se omitió porque no se configuraron secretos de SonarCloud; el análisis local de SonarQube sí está documentado más abajo.

La siguiente ejecución, [CI/CD #36095436798](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095436798), concluyó en éxito con los cuatro jobs: pruebas y cobertura, Docker, calidad y `Deploy staging through Render hook`. El paso `Trigger Render deploy hook` se ejecutó correctamente; así se validó el despliegue automático desde un push a `main` sin revelar el secreto. La última ejecución verificada, [CI/CD #36095583947](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095583947), también finalizó correctamente.

## SonarQube/SonarCloud

El archivo `sonar-project.properties` apunta a `reports/pytest/coverage.xml`; `.coveragerc` usa rutas relativas para que el informe sea compatible con el escáner en contenedor. Para SonarCloud configura `SONAR_TOKEN` y `SONAR_HOST_URL` como secretos de GitHub y ajusta `sonar.projectKey`/organización según tu cuenta. Para SonarQube local, ejecuta `sonar-scanner` después de Pytest con cobertura.

El análisis local verificado con SonarQube Community Build 26.9.0.129388 registró 0 bugs, 0 vulnerabilidades, 0 security hotspots, 0 code smells, 97.4 % de cobertura y 0.0 % de líneas duplicadas. Las respuestas de la API se conservan en `reports/sonar/`.

## OWASP ZAP

Con la API ejecutándose y Docker disponible:

```bash
bash scripts/run_zap.sh http://localhost:8000
```

En PowerShell puedes usar `./scripts/run_zap.ps1 http://host.docker.internal:8000`.

El script usa ZAP API Scan contra `/openapi.json` y guarda sus informes HTML/JSON. La ejecución inicial registró dos tipos de alerta Low: faltaban `X-Content-Type-Options` y `Cross-Origin-Resource-Policy`. La API ahora establece `nosniff` y `same-origin` respectivamente; el reescaneo final registró 0 High, 0 Medium y 0 Low. Los informes comparativos están en `reports/zap/initial/` y `reports/zap/final/`.

## Staging y despliegue

El servicio de staging está publicado en [Render](https://sistema-donaciones-pgju.onrender.com) como Web Service Docker en el plan Free. Usa `DATABASE_URL=sqlite:///./donaciones.db`, una clave JWT privada configurada en Render y `/health` como Health Check Path. El Deploy Hook está almacenado de forma privada en el secreto de GitHub `RENDER_DEPLOY_HOOK_URL`; su valor no se versiona ni se muestra en el repositorio.

Se comprobaron respuestas `200 OK` en [health](https://sistema-donaciones-pgju.onrender.com/health), [docs](https://sistema-donaciones-pgju.onrender.com/docs) y [openapi](https://sistema-donaciones-pgju.onrender.com/openapi.json). La ejecución CI/CD #36095436798 confirmó que un push a `main` invoca correctamente el hook de despliegue. Como es un servicio Free, Render puede requerir un breve arranque después de un periodo de inactividad.

## Evidencias y limitaciones

`RESULTADOS_PARA_INFORME.md` es la fuente de verdad de los resultados finales. `AUDITORIA_FINAL.md` contrasta el resultado con la rúbrica y `CAPTURAS_PENDIENTES.md` indica únicamente las evidencias visuales que requieren una sesión autenticada o interacción manual. Las capturas reales disponibles se guardan en `evidencias/`, sin incluir credenciales.
