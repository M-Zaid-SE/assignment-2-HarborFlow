import re
from pathlib import Path
import json

def show_incidents():
    folder = Path("dataset/incidents")
    choices = []

    for number, f in enumerate(folder.glob("*.json"), start=1): # Enumerate makes the returned printed list numbered.
        with open(f, "r", encoding="utf-8") as file:
            reader = json.load(file)
            incident = reader["incident_id"]
            print(f"{number}. {incident}") # Using an f-string allows adding a dot after each numbered line.
            choices.append(f)
    while True: # Ensures the input loops with sanity checks for non-integer inputs and checks correct range.
        try:
            choice = int(input("Select an incident: "))
        except ValueError:
            print("Error - Select a listed incident.")
            continue

        if len(choices) >= choice >= 1:
            return choices[choice - 1]
        print("Error - Select a listed incident.")



def replacing_container_identifiers(incident):
    copied_file = ""

    with open(incident, "r", encoding="utf-8") as file:
        reader = json.load(file)
        copied_file = copied_file + reader["report"] # Adds the text under "report" key into a string variable
        
    # Substitutes values in accordance to task requirements.
    changed_container = re.sub(r"[A-Za-z]{4}[0-9]{7}", "[CONTAINER]", copied_file)
    changed_seal = re.sub(r"[A-Za-z]{4}[-][0-9]{6}", "[SEAL]", changed_container)
    changed_mail = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[A-Za-z]{2,}", "[EMAIL]", changed_seal)
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
            print(changed_mail)
            print("File saved.")
            return


    


