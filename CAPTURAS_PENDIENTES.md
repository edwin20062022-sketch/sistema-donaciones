# Capturas pendientes de sesión autenticada

Las siguientes capturas no se fabricaron. Las evidencias técnicas equivalentes ya están disponibles en `reports/` y `evidencias/`.

## GitHub Actions

1. Abrir `https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095583947`.
2. Iniciar sesión en GitHub si es necesario.
3. Capturar el resumen de `CI CD` con los cuatro jobs en verde.
4. Guardar como `evidencias/05_github_actions/05_github_actions_success.png`.

## SonarQube Overview

1. Abrir `http://localhost:9000/dashboard?id=sistema-donaciones`.
2. Iniciar sesión en la instancia local de SonarQube.
3. Capturar el Overview donde aparezcan cobertura, bugs, vulnerabilidades, code smells y duplicación.
4. Guardar como `evidencias/04_sonar/04_sonar_overview.png`.

## Flujo interactivo de Swagger

1. Abrir `https://sistema-donaciones-pgju.onrender.com/docs`.
2. Registrar un usuario, iniciar sesión y autorizar el JWT en Swagger.
3. Intentar `GET /donantes` con el usuario normal para mostrar `403 Forbidden`.
4. Guardar como `evidencias/06_staging/06_swagger_login_y_403.png`.
