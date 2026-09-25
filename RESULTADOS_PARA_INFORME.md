# Resultados para el informe

Este archivo concentra datos verificables para completar el Word adjunto. Las cifras se actualizan únicamente después de ejecutar cada herramienta.

## A. Pruebas

* número de pruebas: 12
* pruebas exitosas: 12
* pruebas fallidas: 0
* cobertura global real: 97.36 %
* archivos con menor cobertura: `app/database.py` con 73 %; el resto de los módulos quedó por encima de 90 %.

## B. CI/CD

* workflow: `.github/workflows/ci-cd.yml`
* jobs configurados: tests, build, quality y deploy-staging
* repositorio: `https://github.com/edwin20062022-sketch/sistema-donaciones`
* ejecución inicial: [CI/CD #36094031338](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36094031338), concluida correctamente; Deploy staging se omitió porque todavía no existía el secreto de Render
* ejecución de despliegue: [CI/CD #36095436798](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095436798), concluida correctamente con los cuatro jobs
* resultado final: Tests and coverage (20 s), Docker build (22 s), Sonar quality analysis (18 s) y Deploy staging through Render hook correctos; el paso `Trigger Render deploy hook` se ejecutó correctamente
* artifacts generados: `pytest-reports`
* configuración actual: `RENDER_DEPLOY_HOOK_URL` está registrado como secreto del repositorio; los pushes posteriores a `main` ejecutan el Deploy Hook

## C. Docker

* Docker Desktop instalado: sí, versión 4.59.0 (217644)
* backend utilizado: Docker Desktop con contenedores Linux sobre WSL 2
* versión WSL: 2.3.26.0; kernel 5.15.167.4-microsoft-standard-WSL2
* `docker version`: cliente 29.2.0; Engine 29.2.0; servidor Docker Desktop 4.59.0; Linux/amd64
* prueba `hello-world`: exitosa
* build exitoso: sí
* comando utilizado: `docker build -t sistema-donaciones:latest .`
* imagen: `sistema-donaciones:latest`
* tamaño de imagen: 66,037,843 bytes
* container iniciado: sí
* nombre del container: `sistema-donaciones`
* puerto: `8000:8000`
* `/health`: accesible, `200 OK`, cuerpo `{"status":"ok"}`
* `/docs`: accesible, `200 OK`
* `/openapi.json`: accesible, `200 OK`
* cabeceras verificadas: `X-Content-Type-Options: nosniff` y `Cross-Origin-Resource-Policy: same-origin`
* errores encontrados: el daemon inicialmente no respondía; Docker Desktop fallaba al iniciar por sockets runtime corruptos y por el componente Model Runner/Inference.
* correcciones realizadas: se regeneraron de forma reversible las carpetas runtime afectadas, se desactivó Model Runner con `docker desktop disable model-runner` y se reinició Docker Desktop con WSL 2.

## D. OWASP ZAP

* fecha/ejecución: 24 de septiembre de 2026, contra el contenedor local activo
* tipo de escaneo: ZAP API Scan contra `http://host.docker.internal:8000/openapi.json`
* informe inicial: 0 High, 0 Medium, 2 tipos de alerta Low (4 ocurrencias) y 3 tipos Informational (38 ocurrencias)
* hallazgos Low iniciales: ausencia de `X-Content-Type-Options` y `Cross-Origin-Resource-Policy`, ambos en `/health` y `/openapi.json`
* correcciones realizadas: middleware que establece `X-Content-Type-Options: nosniff` y `Cross-Origin-Resource-Policy: same-origin`; prueba automatizada de dichas cabeceras
* informe final: 0 High, 0 Medium, 0 Low y 3 tipos Informational (38 ocurrencias)
* informativos finales: 31 respuestas 4xx provocadas por el escáner, 5 respuestas no almacenables y 2 respuestas almacenables; sin alertas abiertas de severidad Low o superior
* evidencia: `reports/zap/initial/` y `reports/zap/final/`

## E. Sonar

* ejecución local: SonarQube Community Build 26.9.0.129388 y SonarScanner CLI 8.1.0.6389
* Bugs: 0
* Vulnerabilities: 0
* Security Hotspots: 0
* Code Smells: 0
* Coverage: 97.4 % (227 líneas a cubrir; 6 sin cubrir)
* Duplicated Lines: 0.0 %
* Technical Debt: 0 minutos
* Maintainability: A (rating 1.0)
* Reliability y Security: A (rating 1.0)
* incidencias abiertas: 0; las 7 incidencias iniciales de code smell quedaron `CLOSED/FIXED`
* evidencia: `reports/sonar/measures.json`, `reports/sonar/issues.json` y `reports/sonar/open-issues.json`

## F. Deployment

* URL staging: `https://sistema-donaciones-pgju.onrender.com`
* proveedor: Render, Web Service Docker, plan Free
* servicio: `srv-daqvhjs9v7es738uag5g`
* estado: Live; Health Check Path configurado como `/health`
* configuración: `DATABASE_URL=sqlite:///./donaciones.db` y clave JWT privada definidas en Render; Deploy Hook privado guardado en GitHub como `RENDER_DEPLOY_HOOK_URL`
* evidencia: `/health`, `/docs` y `/openapi.json` respondieron `200 OK`; CI/CD #36095436798 invocó el Deploy Hook correctamente

## G. Evidencias para insertar en Word

1. Swagger mostrando un registro y login exitosos.
2. `/auth/me` mostrando el rol sin exponer el hash.
3. Respuesta `403 Forbidden` al listar donantes con usuario normal.
4. Terminal de Pytest con cobertura real.
5. Ejecución de GitHub Actions en verde.
6. Build o ejecución de la imagen Docker.
7. Reporte HTML/JSON de ZAP.
8. Vista Overview de SonarQube/SonarCloud.
9. Vista de cobertura, code smells y deuda técnica en SonarQube/SonarCloud.
10. URL y estado Live del staging en Render.

## Desviaciones y decisiones técnicas

* El administrador se crea mediante `scripts/create_admin.py` con variables de entorno; el registro público nunca acepta el rol.
* ZAP y SonarQube se ejecutaron localmente con evidencias versionadas. GitHub Actions se ejecutó correctamente y el staging de Render quedó publicado y comprobado.
* La API se inició localmente y respondió `200 OK` en `/health` y `/openapi.json`.
* El documento Word conserva campos pendientes; este repositorio es la fuente de los resultados de ejecución que deben trasladarse al informe.
