import re
import json
from data_access import query_json, DATASET_DIR, INCIDENTS_DIR

CACHE_FILE = DATASET_DIR / "incident-index.json"

def structure():
    index = None
    titles = None

    if CACHE_FILE.exists():
        cache_time = CACHE_FILE.stat().st_mtime
        fresh = True
        for incident_file in INCIDENTS_DIR.glob("*.json"):
            if incident_file.stat().st_mtime > cache_time:
                fresh = False

        if fresh:
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data["index"], data["titles"]
            except(OSError, ValueError, KeyError, TypeError):
                pass

    incidents, _ = query_json("incidents")
    index = {}
    titles = {}

    for incident_id in incidents:
        incident = incidents[incident_id]
        titles[incident_id] = incident["title"]

        text = incident["report"].lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        for word in text.split():
            if word not in index:
                index[word] = []
            if incident_id not in index[word]:
                index[word].append(incident_id)

    for word in index:
        index[word].sort()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"index": index, "titles": titles}, f, indent=2, sort_keys=True)

    return index, titles


def search(query):
    index, titles = structure()

    text = query.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = set(text.split())

    scores = {}

    for word in words:
        if word in index:
            for incident_id in index[word]:
                if incident_id not in scores:
                    scores[incident_id] = 0
                scores[incident_id] += 1

    pairs = []
    for incident_id in scores:
        pairs.append((-scores[incident_id], incident_id))
    pairs.sort()

    print(f"Matches for {query}")
    for negative_score, incident_id in pairs:
        print(f"- {incident_id} | score {-negative_score} | {titles[incident_id]}")

user_search = input("Search incident reports: ")
search(user_search)