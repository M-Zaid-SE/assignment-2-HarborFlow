from pathlib import Path
import json
import csv

# Paths are relative to this file, so they work from any folder
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"


def read_json(folder, required, key):
    '''Reads every .json file in a folder. Returns (dict of records keyed by the key field, skipped file count)'''
    records = {}
    skipped = 0

    for file in Path(folder).glob("*.json"):
        try:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("File does not contain a JSON object.")

            for field in required:
                if field not in data:
                    raise ValueError("Missing required field '" + field + "'.")

            # Fields that must have a specific type
            if "name" in data and not isinstance(data["name"], str):
                raise ValueError("name must be text.")
            if "weight_kg" in data and not isinstance(data["weight_kg"], (int, float)):
                raise ValueError("weight_kg must be a number.")
            if "capacity_teu" in data and not isinstance(data["capacity_teu"], int):
                raise ValueError("capacity_teu must be a whole number.")
            if "shipment_ids" in data and not isinstance(data["shipment_ids"], list):
                raise ValueError("shipment_ids must be a list.")
            if "event_codes" in data and not isinstance(data["event_codes"], list):
                raise ValueError("event_codes must be a list.")

            records[data[key]] = data

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            skipped += 1
            print("Error when reading " + file.name + ": " + str(e))

    return records, skipped


def read_csv(path, required):
    '''Reads a CSV file. Returns (list of rows as dicts, skipped row count)'''
    rows = []
    skipped = 0

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # A row is valid only if every required column has a value
                missing = [field for field in required if not row.get(field)]
                if missing:
                    skipped += 1
                    print("Error when reading CSV row: missing " + missing[0] + ".")
                else:
                    rows.append(row)

    except FileNotFoundError:
        print("Error - Could not find " + Path(path).name)
    except csv.Error as e:
        print("Error when reading " + Path(path).name + ": " + str(e))

    return rows, skipped


def query_json(dataset):
    '''Loads one JSON dataset: vessels, manifests, shipments or incidents.
    Returns (dict of valid records keyed by id, skipped file count)'''
    if dataset == "vessels":
        return read_json(DATASET_DIR / "vessels", ("vessel_id", "name", "imo", "capacity_teu"), "vessel_id")
    elif dataset == "manifests":
        return read_json(DATASET_DIR / "manifests", ("call_id", "vessel_id", "shipment_ids", "event_codes"), "call_id")
    elif dataset == "shipments":
        return read_json(DATASET_DIR / "shipments", ("shipment_id", "customer", "destination", "weight_kg", "priority"), "shipment_id")
    elif dataset == "incidents":
        return read_json(DATASET_DIR / "incidents", ("incident_id", "call_id", "title", "report"), "incident_id")
    else:
        raise ValueError("Unknown JSON dataset '" + dataset + "'.")


def query_csv(dataset):
    '''Loads one CSV dataset: port_calls or weather.
    Returns (list of valid rows, skipped row count)'''
    if dataset == "port_calls":
        return read_csv(DATASET_DIR / "port_calls.csv", ("call_id", "vessel_id", "port_code", "arrival_date"))
    elif dataset == "weather":
        return read_csv(DATASET_DIR / "weather.csv", ("port_code", "date", "wind_kmh", "precipitation_mm", "wave_height_m"))
    else:
        raise ValueError("Unknown CSV dataset '" + dataset + "'.")


def load_vessels(vessels, skipped_files):
    '''Prints the vessels sorted by name, ignoring case'''
    sorted_vessels = sorted(vessels.values(), key=lambda v: v["name"].casefold())

    print("Registered HarborFlow vessels:")
    for vessel in sorted_vessels:
        print("- " + vessel["name"] + " | IMO " + str(vessel["imo"]) + " | " + format(vessel["capacity_teu"], ",") + " TEU")

    print("Skipped vessel files: " + str(skipped_files))
