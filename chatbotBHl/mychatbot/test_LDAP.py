"""Test rapide de connexion LDAP — lit les identifiants depuis .env."""
import os
from pathlib import Path

import ldap
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

ldap_server = os.getenv("LDAP_SERVER", "ldap://127.0.0.1:389")
service_user = os.getenv("LDAP_SERVICE_USER", "")
service_password = os.getenv("LDAP_SERVICE_PASSWORD", "")

try:
    conn = ldap.initialize(ldap_server)
    conn.set_option(ldap.OPT_REFERRALS, 0)
    conn.simple_bind_s(service_user, service_password)
    print("Connexion AD réussie !")
except ldap.INVALID_CREDENTIALS:
    print("Nom d'utilisateur ou mot de passe incorrect")
except Exception as e:
    print(f"Erreur : {e}")
