# Resultados para el informe

Este archivo concentra datos verificables para completar el Word adjunto. Las cifras se actualizan únicamente después de ejecutar cada herramienta.

## A. Pruebas

* número de pruebas: 11
* pruebas exitosas: 11
* pruebas fallidas: 0
* cobertura global real: 96.71 %
* archivos con menor cobertura: `app/database.py` con 73 %; el resto de los módulos quedó por encima de 90 %.

## B. CI/CD

* workflow: `.github/workflows/ci-cd.yml`
* jobs configurados: tests, build, quality y deploy-staging
* resultado de ejecución: PENDIENTE DE EJECUCIÓN REAL EN GITHUB ACTIONS
* artifacts generados: `pytest-reports` cuando el workflow se ejecute

## C. Docker

* build exitoso: No disponible en este entorno; Docker Desktop no tenía iniciado el daemon Linux.
* comando utilizado: `docker build -t sistema-donaciones .`
* resultado: ejecución intentada; falló antes del build con `The system cannot find the file specified` al conectar con `dockerDesktopLinuxEngine`.

## D. OWASP ZAP

* fecha/ejecución: PENDIENTE DE EJECUCIÓN REAL
* tipo de escaneo: ZAP API Scan contra `/openapi.json`
* alertas High: PENDIENTE DE EJECUCIÓN REAL
* alertas Medium: PENDIENTE DE EJECUCIÓN REAL
* alertas Low: PENDIENTE DE EJECUCIÓN REAL
* alertas Informational: PENDIENTE DE EJECUCIÓN REAL
* hallazgos principales: PENDIENTE DE EJECUCIÓN REAL
* correcciones realizadas: PENDIENTE DE EJECUCIÓN REAL
* resultado después de correcciones: PENDIENTE DE EJECUCIÓN REAL

## E. Sonar

* Bugs: PENDIENTE DE EJECUCIÓN REAL
* Vulnerabilities: PENDIENTE DE EJECUCIÓN REAL
* Security Hotspots: PENDIENTE DE EJECUCIÓN REAL
* Code Smells: PENDIENTE DE EJECUCIÓN REAL
* Coverage: PENDIENTE DE EJECUCIÓN REAL
* Duplicated Lines: PENDIENTE DE EJECUCIÓN REAL
* Technical Debt: PENDIENTE DE EJECUCIÓN REAL
* Maintainability: PENDIENTE DE EJECUCIÓN REAL

## F. Deployment

* URL staging: PENDIENTE DE CREDENCIALES Y CONFIGURACIÓN EXTERNA
* proveedor: Render preparado mediante `RENDER_DEPLOY_HOOK_URL`
* fecha: PENDIENTE DE EJECUCIÓN REAL
* estado: PENDIENTE DE EJECUCIÓN REAL
* evidencia: PENDIENTE DE EJECUCIÓN REAL
* pasos pendientes: crear servicio, configurar variables y agregar el secreto en GitHub

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
10. URL y estado del staging, si se configura.

## Desviaciones y decisiones técnicas

* El administrador se crea mediante `scripts/create_admin.py` con variables de entorno; el registro público nunca acepta el rol.
* ZAP, Sonar y staging dependen de herramientas o credenciales externas y no se reportan como ejecutados hasta contar con evidencia real.
* La API se inició localmente y respondió `200 OK` en `/health` y `/openapi.json`.
* El documento Word conserva campos pendientes; este repositorio es la fuente de los resultados de ejecución que deben trasladarse al informe.
