"""Test rapide de connexion Oracle — lit les identifiants depuis .env."""
import os
from pathlib import Path

import cx_Oracle
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

dsn = cx_Oracle.makedsn(
    os.getenv("ORACLE_HOST", "127.0.0.1"),
    int(os.getenv("ORACLE_PORT", "1521")),
    service_name=os.getenv("ORACLE_NAME", ""),
)

try:
    conn = cx_Oracle.connect(
        user=os.getenv("ORACLE_USER", ""),
        password=os.getenv("ORACLE_PASSWORD", ""),
        dsn=dsn,
    )
    print("Connexion réussie !")
    conn.close()
except cx_Oracle.DatabaseError as e:
    print("Erreur de connexion :", e)
