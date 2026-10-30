# Finorix — Chatbot NLP pour BH Leasing

Chatbot web interne permettant aux équipes métier d’interroger des **rapports SQL Oracle** via des questions en **langage naturel**.

> Stage (août–septembre 2025) — BH Leasing, Tunis

## Fonctionnement (en bref)

1. Authentification **Active Directory (LDAP)**
2. Question utilisateur → embeddings **MiniLM** (`all-MiniLM-L6-v2`)
3. Similarité **cosine** avec ~41 rapports (`rapports.json`)
4. Exécution SQL sur **Oracle** (ou résultat **Redis** en cache)
5. Affichage tableau + graphiques (**Chart.js**), filtres, export CSV/XLSX

Ce n’est pas un RAG + LLM classique : c’est un **RAG de rapports** (retrieval → SQL prévalidé → rendu UI).

## Stack

| Couche | Techno |
|---|---|
| Backend | Python, Django |
| NLP | Sentence Transformers (MiniLM) |
| Base métier | Oracle (`cx_Oracle`) |
| Cache | Redis |
| Auth | LDAP / Active Directory |
| Front | HTML/CSS/JS, Bootstrap, Chart.js |

## Structure du dépôt

```text
projet_BHLeasing/
├── README.md
├── .env.example          # modèle de configuration (sans secrets)
├── .gitignore
├── docs/
│   └── Fiche_Finorix_Complete.md   # workflow RAG + Q&R interview
├── scripts/
│   ├── run_chatbot.bat
│   └── wait_server.py
└── chatbotBHl/
    └── mychatbot/        # projet Django
        ├── manage.py
        ├── requirements.txt
        └── chat/
            ├── views.py
            ├── utils.py          # MiniLM + execute_report
            ├── rapports.json     # catalogue des rapports SQL
            └── templates/
```

## Prérequis

- Python 3.10+
- Redis (local ou distant)
- Accès Oracle + LDAP (environnement entreprise), **ou** configuration adaptée
- Client Oracle Instant Client si besoin pour `cx_Oracle`

## Installation

```bash
git clone https://github.com/<TON_USER>/finorix-bhleasing.git
cd finorix-bhleasing

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
# source venv/bin/activate

pip install -r chatbotBHl/mychatbot/requirements.txt
```

### Configuration

```bash
copy .env.example .env
# puis éditer .env avec tes valeurs (SECRET_KEY, Oracle, Redis, LDAP)
```

> **Important :** ne jamais committer `.env`. Les mots de passe et comptes internes ne doivent pas apparaître dans le code.

### Lancer

```bash
cd chatbotBHl/mychatbot
python manage.py migrate
python manage.py runserver
```

Ouvrir : http://127.0.0.1:8000/

## Documentation

Voir [`docs/Fiche_Finorix_Complete.md`](docs/Fiche_Finorix_Complete.md) :

- Workflow & schéma RAG
- Pourquoi MiniLM / cosine (vs L2)
- Questions & réponses d’interview

## Auteur

Projet réalisé dans le cadre d’un stage chez **BH Leasing**.
