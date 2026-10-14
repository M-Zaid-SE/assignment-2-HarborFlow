from pathlib import Path
import json, csv

# CONSTANTS:
BASE_DIR = Path(__file__).resolve().parent # Derives full file path for all containd in proj
DATASET_DIR = BASE_DIR / "dataset"
INCIDENTS_DIR = DATASET_DIR / "incidents"
MANIFESTS_DIR = DATASET_DIR / "manifests"
SHIPMENTS_DIR = DATASET_DIR / "shipments"
VESSELS_DIR = DATASET_DIR / "vessels"
PORT_CALLS_FILE = DATASET_DIR / "port_calls.csv"
WEATHER_FILE = DATASET_DIR / "weather.csv"

# Dataset name -> (folder, required fields, unique id field used as dict key)
JSON_DATASETS = {
    "vessels":   (VESSELS_DIR,   ("vessel_id", "name", "imo", "capacity_teu"), "vessel_id"),
    "manifests": (MANIFESTS_DIR, ("call_id", "vessel_id", "shipment_ids", "event_codes"), "call_id"),
    "shipments": (SHIPMENTS_DIR, ("shipment_id", "customer", "destination", "weight_kg", "priority"), "shipment_id"),
    "incidents": (INCIDENTS_DIR, ("incident_id", "call_id", "title", "report"), "incident_id"),
}

# Dataset name -> (file, required columns)
CSV_DATASETS = {
    "port_calls": (PORT_CALLS_FILE, ("call_id", "vessel_id", "port_code", "arrival_date")),
    "weather":    (WEATHER_FILE,    ("port_code", "date", "wind_kmh", "precipitation_mm", "wave_height_m")),
}

# Required JSON fields that must have a specific type, checked when reading
FIELD_TYPES = {
    "name": str,
    "capacity_teu": int,
    "weight_kg": (int, float),
    "shipment_ids": list,
    "event_codes": list,
}

def read_json(path, req = None, key = None):
    '''Takes a filepath, required JSON fields (optional) & id field to key by (optional) as args and returns json object(s)'''
    json_data = {}  
    skipped_files = 0
    filelist = Path(path).glob('*.json')

    for file in filelist:
        try:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict): # File must hold one JSON object, not a list or number
                    raise ValueError("File does not contain a JSON object.")

                if req: # Check if any requirements were passed as args at call
                    for entry in req:
                        if entry not in data: # Checks that every str in req exists as a field in data
                            raise ValueError(f"Missing required field '{entry}'.")
                        if entry in FIELD_TYPES and not isinstance(data[entry], FIELD_TYPES[entry]):
                            raise ValueError(f"Field '{entry}' has the wrong type.")

                json_data.update({data[key] if key else file.stem: data}) # Adds json to dict using id field (or filename) as key

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            skipped_files += 1
            print(f"Error when reading {file.name}: {e}")

    return(json_data, skipped_files)


def read_csv(path, req = None):
    '''Takes a CSV filepath & required columns (optional) as args and returns list of rows as dicts'''
    csv_data = []
    skipped_rows = 0

    try:
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f) # Uses header row as keys for each row dict

            for row in reader:
                try:
                    if req: # Check if any requirements were passed as args at call
                        for entry in req:
                            if not row.get(entry): # Checks that every str in req exists and has a value in row
                                raise ValueError(f"Row is missing required field '{entry}'.")

                    csv_data.append(row)

                except ValueError as e:
                    skipped_rows += 1
                    print(f"Error when reading CSV row: {e}")

    except FileNotFoundError:
        print(f"Error - Could not find {Path(path).name}") # Only file name, no absolute path
    except (csv.Error, ValueError) as e:
        print(f"Error when reading {Path(path).name}: {e}")

    return(csv_data, skipped_rows)

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
        print(f"- {name} | IMO {vessel['imo']} | {vessel['capacity_teu']:,} TEU")

    print(f"Skipped vessel files: {skipped_files}")
    return

def query_json(dataset):
    '''Takes a JSON dataset name and returns (dict of valid JSON objects keyed by their id, skipped file count):
    vessels, manifests, shipments, incidents. '''

    if dataset not in JSON_DATASETS:
        raise ValueError(f"Unknown JSON dataset '{dataset}'. Choose from: {', '.join(JSON_DATASETS)}")

    path, req, key = JSON_DATASETS[dataset]
    return read_json(path, req, key)

def query_csv(dataset):
    '''Takes a CSV dataset name and returns (list of valid rows, skipped row count):
    port_calls, weather.'''
    
    if dataset not in CSV_DATASETS:
        raise ValueError(f"Unknown CSV dataset '{dataset}'. Choose from: {', '.join(CSV_DATASETS)}")

    path, req = CSV_DATASETS[dataset]
    return read_csv(path, req)
    