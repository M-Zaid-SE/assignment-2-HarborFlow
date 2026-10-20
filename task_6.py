import re
from pathlib import Path
import json

def show_incidents():
    folder = Path("dataset/incidents")
    incidents = []

    for filepath in folder.glob("*.json"): # Loops through all .json files in folder
        with open(filepath, "r", encoding="utf-8") as file:
            record = json.load(file)
        incidents.append((record["title"], filepath)) # Adds the title and the filepath where that title is found to a tuple inside the incidents list.

    incidents.sort() # Sorts alphabetically.

    for number, (title, filepath) in enumerate(incidents, start=1): # Enumerate adds numbers for each line. 
        print(f"{number}. {title}")

    while True:
        try:
            choice = int(input("Select an incident: "))
            if 1 <= choice <= len(incidents):
                return incidents[choice -1][1] # Returns the path to the chosen file. Indexing into the tuple (-1 to account for 0 start) [1] points at "filepath" in incidents.
            else:
                print("Error select a listed incident.")
                continue
        except ValueError:
            print("Error select a listed incident.")
            continue



def replacing_container_identifiers(incident):
    copied_file = ""

    with open(incident, "r", encoding="utf-8") as file:
        reader = json.load(file)
        copied_file = copied_file + reader["report"] # Adds the text under "report" key into a string variable
        
    # Substitutes values in accordance to task requirements.
    changed_container = re.sub(r"[A-Za-z]{4}[0-9]{7}", "[CONTAINER]", copied_file)
    changed_seal = re.sub(r"SEAL-[0-9]{6}", "[SEAL]", changed_container)
    changed_mail = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]", changed_seal)
    return changed_mail, incident, copied_file


def write_file(changed_mail, incident, copied_file):
    if copied_file == changed_mail: # Ensures that no file is created if nothing was substituted from the original incident report
        print("Incident contains no share-sensitive identifiers.")
        return
    else:
        folder = Path("exports/sanitized")
        folder.mkdir(parents=True, exist_ok=True) # Checks if the exports/sanitized folder exists. Creates it if it doesn't, doesn't do anything if it does.

        with open(incident, "r", encoding="utf-8") as file:
            reader = json.load(file)
            incident_name = reader["incident_id"] # Assigns the relevant incident id to a string variable to allow for correct file name creation further down in the block
            reader["report"] = changed_mail # Changes the text under the "report" key into the newly sanitized version.
            
        with open(folder / (incident_name + "-sanitized.txt"), "w", encoding="utf-8") as file:
            file.write(changed_mail)
            print("Incident sanitized.")
            return


    


