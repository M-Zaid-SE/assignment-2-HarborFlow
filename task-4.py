from pathlib import Path
import csv, json

def match_name(name):
    folder = Path("dataset/shipments") 
    data = {}
    found_in = []

    for f in sorted(folder.glob("*.json")):
        with open(f, "r", encoding="utf-8") as file:
            data[f.name] = json.load(file)


    for filename, record in data.items():
        if record["customer"].strip().lower() == name.strip().lower():
            found_in.append(filename)
            
    return found_in


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

    destinations_list.sort()
    destinations = "|".join(destinations_list)    
    return shipment_count_total, total_weight_kg, express_count, destinations
            

def add_profile(name, shipment_count_total, total_weight_kg, express_count, destinations):
    customer_profiles = "exports/customer-profiles.csv"
    new_row = [name, shipment_count_total, total_weight_kg, express_count, destinations]
    header = ["customer", "shipment_count", "total_weight_kg", "express_count", "destinations"]
    rows = []
    found = False

    with open(customer_profiles, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0].strip().lower() == name.strip().lower():
                found = True
                rows.append(new_row)
            else:
                rows.append(row)

    if not found:
        with open(customer_profiles, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
    else:
        with open(customer_profiles, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)




name = input("Customer name: ")

found_in = match_name(name)
check_file_exists()
shipment_count_total, total_weight_kg, express_count, destinations = calculations(found_in)
add_profile(name, shipment_count_total, total_weight_kg, express_count, destinations)

print("Customer profile updated: exports/customerprofiles-csv")



