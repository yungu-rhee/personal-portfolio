# Local SQL Pipeline

Pipeline mínimo de lectura/escritura sobre SQL Server aplicando buenas prácticas de data engineering: configuración externalizada, contenedores, tests y CI. (Para estudio personal)

## Arquitectura

```
┌─────────────────┐        ┌──────────────────┐        ┌─────────────────┐
│  generate/write │ ─────> │   SQL Server     │ ─────> │      read       │
│  (src/write.py) │ insert │  (Docker, local) │ select │  (src/read.py)  │
└─────────────────┘        └──────────────────┘        └─────────────────┘
```

- **SQL Server 2022** corre en un contenedor Docker (Developer Edition, gratuita).
- **write.py** genera precios horarios simulados del mercado eléctrico y los inserta de forma idempotente (borra el día antes de insertar).
- **read.py** consulta la tabla y muestra un resumen por día.
- **pytest** valida la lógica.
- **GitHub Actions** ejecuta lint y tests en cada push.

## Requisitos

- Docker Desktop
- Python 3.11+
- ODBC Driver 17 o 18 for SQL Server

## Puesta en marcha

```bash
# 1. Copiar la plantilla de configuración y ajustar si es necesario
cp .env.example .env

# 2. Levantar SQL Server
docker compose up -d

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el esquema y la tabla (espera ~30s a que SQL Server arranque)
python src/init_db.py

# 5. Escribir datos simulados
python src/write.py

# 6. Leer
python src/read.py

# 7. Tests
pytest
```

## Estructura

```
local-sql-pipeline/
├── .github/workflows/ci.yml   # CI: lint + tests en cada push
├── docker-compose.yml          # SQL Server 2022 en contenedor
├── Dockerfile                  # Imagen del código Python
├── .env.example                # Plantilla de configuración
├── requirements.txt
├── sql/ddl.sql                 # Esquema y tabla
├── src/
│   ├── config.py               # Carga de configuración desde .env
│   ├── generate.py             # Lógica pura de generación de datos
│   ├── db.py                   # Conexión centralizada
│   ├── init_db.py              # Ejecuta el DDL
│   ├── write.py                # Genera e inserta datos simulados
│   └── read.py                 # Consulta y muestra resumen
└── tests/test_pipeline.py      # pytest
```

## Buenas prácticas aplicadas

- **Configuración externalizada**: credenciales y conexión en `.env`, nunca en el código. `.env` está en `.gitignore`; solo se versiona la plantilla `.env.example`.
- **Conexión centralizada**: un único punto (`src/db.py`) construye la conexión; el resto del código lo reutiliza.
- **Idempotencia**: reejecutar `write.py` para el mismo día no duplica datos (delete + insert por fecha).
- **Inserts parametrizados**: sin concatenación de SQL, previene inyección.
- **Inserción por lotes**: `executemany` con `fast_executemany` en vez de inserts fila a fila.
- **Tests**: la lógica de generación y agregación se prueba sin necesidad de base de datos.
- **CI**: GitHub Actions ejecuta ruff (lint) y pytest en cada push.
- **Contenedores**: la base de datos es reproducible en cualquier máquina con `docker compose up`.
