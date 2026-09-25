# Resultados verificables para el informe final

Este archivo es la fuente de verdad para el informe y la entrega. Los valores proceden de ejecuciones locales, reportes versionados y servicios publicados; no contiene secretos.

## A. Aplicación

* tecnología: Python 3.12, FastAPI, SQLAlchemy, SQLite, Pydantic, JWT y Argon2.
* endpoints: `/health`, `/docs`, `/openapi.json`, `/auth/register`, `/auth/login`, `/auth/me` y CRUD de `/donantes`.
* autenticación: JWT con expiración; las contraseñas se almacenan con Argon2.
* roles: `user` y `admin`; el listado, actualización y eliminación administrativa se protegen por rol.
* base de datos: SQLite mediante SQLAlchemy. Las pruebas usan una base aislada.

## B. Pruebas

* comando final: `python -m pytest tests -p no:cacheprovider --cov=app --cov-report=term-missing --cov-report=html:reports/pytest/htmlcov --cov-report=xml:reports/pytest/coverage.xml --cov-fail-under=80`.
* ejecución final: 12 pruebas ejecutadas, 12 exitosas y 0 fallidas.
* cobertura global real: 97.36 % (221 de 227 líneas cubiertas).
* menor cobertura: `app/database.py`, 73 %; contiene inicialización de base de datos no recorrida en todas las ramas por la suite.
* evidencia: `reports/pytest/coverage.xml`, `reports/pytest/htmlcov/` y `evidencias/01_pytest/01_pytest_cobertura.png`.

## C. Docker

* Docker Desktop: 4.59.0 (217644), Engine 29.2.0, backend Linux `overlayfs` sobre WSL 2 (kernel 5.15.167.4-microsoft-standard-WSL2).
* `docker run --rm hello-world`: exitoso.
* build final: `docker build -t sistema-donaciones:latest .`, exitoso.
* imagen: `sistema-donaciones:latest`, 66,037,843 bytes.
* contenedor activo: `sistema-donaciones`, puerto `8000:8000`.
* endpoints locales verificados: `/health`, `/docs` y `/openapi.json`, todos con `200 OK`.
* cabeceras verificadas: `X-Content-Type-Options: nosniff` y `Cross-Origin-Resource-Policy: same-origin`.

## D. OWASP ZAP

* ejecución: 24 de septiembre de 2026; ZAP API Scan contra `http://host.docker.internal:8000/openapi.json`.
* informe inicial: 0 High, 0 Medium, 2 tipos Low (4 ocurrencias) y 3 tipos Informational (38 ocurrencias).
* hallazgos Low iniciales: ausencia de `X-Content-Type-Options` y `Cross-Origin-Resource-Policy` en `/health` y `/openapi.json`.
* corrección: middleware que añade `nosniff` y `same-origin`, con prueba automatizada.
* informe final: 0 High, 0 Medium, 0 Low y 3 tipos Informational (38 ocurrencias).
* informativos finales: 31 respuestas 4xx provocadas por el escáner, 5 respuestas no almacenables y 2 respuestas almacenables; no hay alertas abiertas Low o superiores.
* evidencia: `reports/zap/initial/`, `reports/zap/final/` y `evidencias/03_zap/03_zap_resultado_final.png`.

## E. SonarQube

* ejecución local: SonarQube Community Build 26.9.0.129388 y SonarScanner CLI 8.1.0.6389.
* Bugs: 0; Vulnerabilities: 0; Security Hotspots: 0; Code Smells: 0.
* Coverage: 97.4 % (227 líneas a cubrir; 6 sin cubrir).
* Duplicated Lines: 0.0 %; Technical Debt: 0 minutos.
* Maintainability, Reliability y Security: A (rating 1.0).
* incidencias abiertas: 0; 7 incidencias iniciales de code smell quedaron `CLOSED/FIXED`.
* evidencia: `reports/sonar/measures.json`, `reports/sonar/issues.json`, `reports/sonar/open-issues.json` y `evidencias/04_sonar/04_sonar_metricas.png`.

## F. GitHub y CI/CD

* repositorio: `https://github.com/edwin20062022-sketch/sistema-donaciones`, rama `main`.
* workflow: `.github/workflows/ci-cd.yml`; jobs `Tests and coverage`, `Docker build`, `Sonar quality analysis` y `Deploy staging through Render hook`.
* ejecución de despliegue verificada: [CI/CD #36095436798](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095436798), concluida correctamente; `Trigger Render deploy hook` se ejecutó correctamente.
* última ejecución verificada: [CI/CD #36095583947](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095583947), concluida correctamente.
* calidad en CI: el escaneo externo de Sonar se condiciona a `SONAR_TOKEN` y `SONAR_HOST_URL`, que no se configuraron; el análisis SonarQube local de la sección E sí se ejecutó y conserva sus métricas reales.
* secreto de despliegue: `RENDER_DEPLOY_HOOK_URL` está configurado en GitHub y no se incluye en el repositorio.

## G. Staging

* proveedor: Render, Web Service Docker, plan Free; servicio `srv-daqvhjs9v7es738uag5g`.
* URL: `https://sistema-donaciones-pgju.onrender.com`.
* estado verificado: Live; Health Check Path `/health`.
* endpoints verificados: `/health`, `/docs` y `/openapi.json`, todos con `200 OK`.
* despliegue automático: demostrado por CI/CD #36095436798 mediante el Deploy Hook de Render.
* evidencia: `evidencias/06_staging/06_staging_docs.png`.

## H. Planificado versus ejecutado

| Actividad planificada | Resultado ejecutado | Desviación técnica | Causa |
| --- | --- | --- | --- |
| Implementación segura, JWT, roles y CRUD | Completado y cubierto por 12 pruebas | Sin tiempo cuantificable | No se registraron tiempos por actividad. |
| Cobertura mínima de 80 % | 97.36 % | Meta superada | Pruebas de flujos correctos y de error. |
| CI/CD, build y deploy | Workflow exitoso y hook de Render ejecutado | Sin tiempo cuantificable | La duración se registra por job, no por fase académica. |
| OWASP ZAP y correcciones | Reescaneo final sin alertas Low o superiores | Sin tiempo cuantificable | Se corrigieron cabeceras detectadas en el primer escaneo. |
| SonarQube y cierre | Métricas finales sin incidencias abiertas | Sin tiempo cuantificable | Análisis local conservado en reportes JSON. |

## I. Lecciones aprendidas

* La cobertura debe conservar rutas portables para que Pytest y Sonar consuman el mismo XML en local y CI.
* Una cobertura alta no sustituye la evaluación de la superficie HTTP: ZAP detectó cabeceras que las pruebas funcionales no habían señalado.
* Las variables privadas del despliegue deben permanecer en Render y GitHub Secrets; el Deploy Hook se validó sin versionar su URL.
* El plan Free de Render puede entrar en reposo; `/health` permitió comprobar el servicio tras su reactivación.

## J. Evidencias y limitaciones de captura

* disponibles: cobertura Pytest, reporte final ZAP, exportación de métricas Sonar y Swagger del staging en `evidencias/`.
* reportes completos: `reports/pytest/`, `reports/zap/` y `reports/sonar/`.
* capturas visuales manuales pendientes: `CAPTURAS_PENDIENTES.md` documenta únicamente las que requieren una sesión autenticada de GitHub o SonarQube, o una interacción manual de Swagger.
