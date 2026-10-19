from pathlib import Path
import csv, json

def match_name(name):
    folder = Path("dataset/shipments") 
    data = {}
    found_in = []

    for f in folder.glob("*.json"): # Loops through all .json files under trajectory
        with open(f, "r", encoding="utf-8") as file:
            data[f.name] = json.load(file) # Store the parsed shipment record in data, keyed by its file name.


    for filename, record in data.items(): # Data.items() gives each key and value pair, filename and record.
        if record["customer"].strip().lower() == name.strip().lower():
            found_in.append(filename)
            
    return found_in # Returns list of files that contain entered customer


def check_file_exists():
    customer_profiles = Path("exports/customer-profiles.csv")
    customer_profiles_path = Path("exports")
    header = ["customer", "shipment_count", "total_weight_kg", "express_count", "destinations"]

    if customer_profiles.exists():
        return
    elif customer_profiles.exists() is False:
        with open(customer_profiles_path / "customer-profiles.csv", "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(header)
            return


def calculations(found_in):
    folder = Path("dataset/shipments")
    shipment_count_total = 0
    total_weight_kg = 0
    express_count = 0
    destinations_list = []

    for each_file in found_in:
        with open(folder / each_file, "r", encoding="utf-8") as file:
            record = json.load(file)

        shipment_count_total += 1
        total_weight_kg += record["weight_kg"]
        if record["priority"] == "EXPRESS":
            express_count += 1
        destinations_list.append(record["destination"])

    destinations_list.sort() # Sorts the list of destinations alphabetically
    destinations = "|".join(destinations_list) # Joins the list with required symbol
    return shipment_count_total, total_weight_kg, express_count, destinations # Returns relevant values
            

def add_profile(name, shipment_count_total, total_weight_kg, express_count, destinations):
    customer_profiles = "exports/customer-profiles.csv"
    new_row = [name, shipment_count_total, total_weight_kg, express_count, destinations]
    header = ["customer", "shipment_count", "total_weight_kg", "express_count", "destinations"]
    rows = []
    found = False

    with open(customer_profiles, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None) # Skips first row, the header.
        for row in reader:
            if row[0].strip().lower() == name.strip().lower():
                found = True # I.e if customer exists
                rows.append(new_row) # Adds the new data into the empty list, rows. Does not add old data.
            else:
                rows.append(row) # Adds any existing data in the .csv into the list for safekeeping

    if not found:
        with open(customer_profiles, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(new_row) # Adds new row at bottom of .csv if customer didn't exist beforehand
    else:
        with open(customer_profiles, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header) # Adds the header back, write overwrites all previous data
            writer.writerows(rows) # Rewrites all other rows including those we safekept earlier.








