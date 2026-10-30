# chat/preload_cache.py
import os
import json
from django.core.cache import cache
from .utils import find_best_report, execute_report

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "reports_history.json")

def preload_reports():
    """Précharge tous les reports dans le cache au démarrage."""
    if not os.path.exists(HISTORY_FILE):
        print("[CACHE] Aucun historique de reports trouvé.")
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    for entry in history:
        report_id = entry.get("report_id")
        cache_key = f"report_{report_id}"
        if cache.get(cache_key):
            continue  # déjà en cache

        params = entry.get("params", {})
        report = find_best_report(params.get("prompt", ""))
        if report:
            result = execute_report(report, params)
            cache.set(cache_key, result, timeout=3600)
            print(f"[CACHE] Préchargé report {report_id}")
