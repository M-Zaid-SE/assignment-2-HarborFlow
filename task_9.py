import re
import json
from data_access import query_json, DATASET_DIR, INCIDENTS_DIR

# Path to the cache file (only builds the address, doesn't create the file)
CACHE_FILE = DATASET_DIR / "incident-index.json"

def structure():
    index = None
    titles = None

    # Only possible if the file exists and no incident file is newer than it.
    # st_mtime is the last-modified time as a number (bigger = more recent).
    if CACHE_FILE.exists():
        cache_time = CACHE_FILE.stat().st_mtime
        fresh = True
        for incident_file in INCIDENTS_DIR.glob("*.json"):  # every .json file in the incidents folder
            if incident_file.stat().st_mtime > cache_time:
                fresh = False  # an incident file changed after the cache was saved

        if fresh:
            # try/except: if the cache is broken, don't crash, just fall through and rebuild.
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data["index"], data["titles"]  # return ends the function, so reports are never reread
            except(OSError, ValueError, KeyError, TypeError):
                pass  # do nothing, continue to the rebuild below

    # (the _ just ignores the skipped-files count that query_json also returns)
    incidents, _ = query_json("incidents")
    index = {}
    titles = {} 

    for incident_id in incidents:
        incident = incidents[incident_id]
        titles[incident_id] = incident["title"]

        # Clean the report: lowercase, then replace anything that isn't
        # a letter, digit or whitespace (i.e. punctuation) with a space
        text = incident["report"].lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # Add this incident's ID to the list of every word it contains
        for word in text.split():
            if word not in index:
                index[word] = []
            if incident_id not in index[word]:
                index[word].append(incident_id)

    # Sort each word's list of IDs (done after building so it's only done once per word)
    for word in index:
        index[word].sort()

    # indent=2 makes the file readable, sort_keys=True sorts the word and title keys
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"index": index, "titles": titles}, f, indent=2, sort_keys=True)

    return index, titles


def search(query):
    # Get the index and titles (from the cache if possible, otherwise rebuilt)
    index, titles = structure()

    # set() removes duplicate words so each query word only counts once.
    text = query.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = set(text.split())

    # Each query word adds 1 point to every incident whose list contains it.
    # Incidents that match nothing never get added, so only positive matches remain.
    scores = {}
    for word in words:
        if word in index:
            for incident_id in index[word]:
                if incident_id not in scores:
                    scores[incident_id] = 0
                scores[incident_id] += 1

    # Each pair is (negative score, ID). Python sorts smallest first, so the most
    # negative number (highest score) comes first, and ties are sorted by ID.
    pairs = []
    for incident_id in scores:
        pairs.append((-scores[incident_id], incident_id))
    pairs.sort()

    # -negative_score flips the score back to positive for display.
    # The title comes from the loaded titles lookup, not from the reports.
    print(f"Matches for '{query}':")
    for negative_score, incident_id in pairs:
        print(f"- {incident_id} | score {-negative_score} | {titles[incident_id]}")