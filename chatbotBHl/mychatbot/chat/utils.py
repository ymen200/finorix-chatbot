# chat/utils.py
import json
from django.conf import settings
import cx_Oracle
from sentence_transformers import SentenceTransformer, util
import os

# Chemin vers le JSON dans le même dossier que utils.py
JSON_PATH = os.path.join(os.path.dirname(__file__), "rapports.json")

# Charger les rapports
with open(JSON_PATH, "r", encoding="utf-8") as f:
    reports = json.load(f)

# Initialiser le modèle d'embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Préparer un embedding par rapport (titre + description + exemples_questions)
report_texts = []
for r in reports:
    combined_text = r["titre"] + ". " + r["description"] + ". " + " ".join(r.get("exemples_questions", []))
    report_texts.append(combined_text)

# Créer embeddings pour tous les rapports
embeddings = model.encode(report_texts, convert_to_tensor=True)

def find_best_report(user_prompt):
    """
    Retourne le rapport le plus pertinent pour un prompt utilisateur
    en utilisant le titre, la description et les exemples de questions.
    """
    user_emb = model.encode(user_prompt, convert_to_tensor=True)
    scores = util.cos_sim(user_emb, embeddings)[0]
    idx = scores.argmax().item()
    return reports[idx]

def execute_report(report, params, row_limit=6000):
    """
    Exécute la requête SQL du rapport avec une limite de lignes.
    Connexion Oracle fixée pour utiliser la config 'oracle' dans settings.py.
    """
    # Récupérer la configuration Oracle
    oracle_db = settings.DATABASES['oracle']

    # Créer DSN Oracle
    dsn = cx_Oracle.makedsn(
        host=oracle_db['HOST'],
        port=int(oracle_db['PORT']),
        service_name=oracle_db['NAME']  # Utilise SID à la place de service_name si nécessaire
    )

    # Connexion à Oracle
    conn = cx_Oracle.connect(
        user=oracle_db['USER'],
        password=oracle_db['PASSWORD'],
        dsn=dsn
    )
    cursor = conn.cursor()

    query = report["requete_sql"]

    # Ajouter limite si pas déjà dans la requête
    limited_query = f"""
        SELECT * FROM (
            {query}
        ) WHERE ROWNUM <= {row_limit}
    """

    cursor.execute(limited_query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Retourner les résultats sous forme de liste de dictionnaires
    results = [dict(zip(columns, row)) for row in data]
    return results
