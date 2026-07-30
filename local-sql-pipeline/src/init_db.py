"""
Inicialización de la base de datos.
Ejecuta sql/ddl.sql contra el servidor (conectando a 'master' porque
la base de datos energydb aún no existe la primera vez).
"""

import logging
from pathlib import Path

import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DDL_PATH = Path(__file__).parent.parent / "sql" / "ddl.sql"


def run_ddl() -> None:
    """Lee el DDL y lo ejecuta batch a batch (separados por GO)."""
    ddl = DDL_PATH.read_text(encoding="utf-8")

    # pyodbc no entiende GO (es un separador de sqlcmd, no de T-SQL),
    # así que troceamos el script y ejecutamos cada batch por separado.
    batches = [b.strip() for b in ddl.split("GO") if b.strip()]

    conn = db.get_connection(database="master")
    conn.autocommit = True  # CREATE DATABASE no puede ir dentro de una transacción
    cursor = conn.cursor()

    for i, batch in enumerate(batches, 1):
        log.info(f"Ejecutando batch {i}/{len(batches)}...")
        cursor.execute(batch)

    conn.close()
    log.info("DDL ejecutado correctamente.")


if __name__ == "__main__":
    run_ddl()
