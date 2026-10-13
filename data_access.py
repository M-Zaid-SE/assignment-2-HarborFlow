from pathlib import Path
import json, csv

# CONSTANTS:
BASE_DIR = Path(__file__).resolve().parent # Derives full file path for all containd in proj
DATASET_DIR = BASE_DIR / "dataset"
INCIDENTS_DIR = DATASET_DIR / "incidents"
MANIFESTS_DIR = DATASET_DIR / "manifests"
SHIPMENTS_DIR = DATASET_DIR / "shipments"
VESSELS_DIR = DATASET_DIR / "vessels"
VESSELS_REQ = ("vessel_id", "name", "imo", "capacity_teu")

def read_json(path, req = None):
    '''Takes a filepath & required JSON fields (optional) as args and returns json object(s)'''
    json_data = {}  
    skipped_files = 0
    filelist = Path(path).glob('*.json')

    for file in filelist:
        try:
            with open(file) as f:
                data = json.load(f)
                if req: # Check if any requirements were passed as args at call
                    for entry in req:
                        if not data[entry]: # Checks that every str in req exists as a field in data 
                            raise Exception("File is missing requireed fields.")

                json_data.update({data["vessel_id"]: data}) # Adds json to dict using vessel_id as key

        except Exception as e:
            skipped_files += 1
            print(f"Error when reading JSON file: {e}")

    return(json_data, skipped_files)


def load_vessels(json_data, skipped_files):
    '''Takes dict of JSON objects and outputs sanitised list'''
    vessel_by_name = []

    for vessel_id, vessel in json_data.items(): # Extract 'name' and 'key' from each vessel. Sort by names, save which key corresponds 
        vessel_by_name.append((vessel["name"], vessel_id))

    vessel_by_name.sort(key=lambda pair: pair[0].casefold())
    
    # Printing all data:
    print("Registered HarborFlow vessels:")
    for name, vessel_id in vessel_by_name:
        vessel = json_data[vessel_id]
        print(f"- {name} | {vessel['imo']} | {vessel['capacity_teu']:,} TEU")

    print(f"Skipped vessel files: {skipped_files}")
    return

load_vessels(*read_json(VESSELS_DIR, VESSELS_REQ))