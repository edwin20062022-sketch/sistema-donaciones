# Auditoría final contra la rúbrica

| Criterio | Evidencia | Estado | Archivo o URL |
| --- | --- | --- | --- |
| Implementación y seguridad | FastAPI, JWT, Argon2, roles y CRUD; 12 pruebas con 97.36 % de cobertura | CUMPLIDO | `app/`, `tests/`, `reports/pytest/` |
| CI/CD | Pruebas, build Docker, calidad condicionada y Deploy Hook ejecutado | CUMPLIDO | `.github/workflows/ci-cd.yml`, [CI/CD #36095583947](https://github.com/edwin20062022-sketch/sistema-donaciones/actions/runs/36095583947) |
| Seguridad y calidad | ZAP inicial/final y SonarQube local con métricas exportadas | CUMPLIDO | `reports/zap/`, `reports/sonar/` |
| Cierre del proyecto | Resultados, lecciones y comparación planificada/ejecutada documentados | PARCIAL | No hay tiempos reales por actividad; se documenta como no cuantificable en vez de inventarlo. |
| Mejora continua | Plan con acciones, indicadores, metas e innovación | CUMPLIDO | `Informe_Final_Sistema_Donaciones_ENTREGA.docx`, sección 13 |

## Revisión de secretos

Se revisaron `.gitignore`, `.env.example` y el contenido versionado. No se incluye `.env`, tokens, URL del Deploy Hook ni claves JWT. Las menciones a `TOKEN`, `SECRET` o `PASSWORD` corresponden a nombres de variables de entorno, documentación o ejemplos.
