# Imports
from datetime import datetime
import data_access
import task_3
import task_5
# Constants


#Task 0
def menu(): 
    options = [
    "1. List registered vessels",
    "2. Inspect a vessel manifest",
    "3. Identify priority cargo",
    "4. Export a customer operations profile",
    "5. Find port calls by month",
    "6. Sanitize an incident report",
    "7. Analyze the longest stable event sequence",
    "8. Assess weather risk for upcoming calls",
    "9. Search incident reports",
    "10. Close console"
]

    print("HARBORFLOW PORT INTELLIGENCE")
    for option in options:
        print(option)
       
    choice = input("Select service: ")

    while choice.isdigit is False or int(choice) < 1 or int(choice) > 10:
        print("Invalid choice - Try Again")
        choice = input("Select service: ")

    return int(choice)

def parse_date(text):
    '''Takes a date string and returns a date object. Raises ValueError unless it is exactly YYYY-MM-DD'''
    if len(text) != 10: # strptime alone accepts short forms like 2026-10-1
        raise ValueError(f"'{text}' does not use YYYY-MM-DD")
    return datetime.strptime(text, "%Y-%m-%d").date()

# Task 2
def inspect_manifest(): 
    vessel_id, call_date = None, None

    vessels, skipped_vessels = data_access.query_json("vessels")
    port_calls, _ = data_access.query_csv("port_calls")

    data_access.load_vessels(vessels, skipped_vessels) # Display available vessels

    # Match name case-insensitively. Unknown vessel returns to menu.
    input_vessel = input("Vessel name: ").strip().casefold()
    for vid, vessel in vessels.items():
        if vessel["name"].casefold() == input_vessel:
            vessel_id = vid
            break
    if not vessel_id:
        print("Vessel not found.")
        return None

    while not call_date: # Invalid date repeats only the date prompt
        input_date = input("Reference date (YYYY-MM-DD): ")
        try:
            call_date = parse_date(input_date.strip())
        except ValueError: print("Error - Date must use YYYY-MM-DD.")

    # Find this vessel's earliest port call on or after the reference date
    arrival, call = None, None
    for row in port_calls:
        if row["vessel_id"] != vessel_id: continue
        try:
            row_date = parse_date(row["arrival_date"]) # CSV dates are strings
        except ValueError as e:
            print(f"Skipping port call {row['call_id']}: {e}") # Invalid date in dataset
            continue
        if row_date < call_date: continue # Call is before the reference date

        # Keep the earliest date, alphabetically smallest call_id breaks ties
        if call is None or arrival is None: # First upcoming call found
            arrival, call = row_date, row
        elif row_date < arrival or (row_date == arrival and row["call_id"] < call["call_id"]):
            arrival, call = row_date, row

    if call is None or arrival is None:
        print("No upcoming port calls found.")
        return None

    manifests, _ = data_access.query_json("manifests") # Keyed by call_id read from file, not filename
    manifest = manifests.get(call["call_id"])
    if not manifest:
        print("Manifest unavailable.")
        return None

    shipments, _ = data_access.query_json("shipments") # Keyed by shipment_id

    print(f"Manifest for {vessels[vessel_id]['name']} | Call {call['call_id']} | {arrival.strftime('%d %B %Y')}")

    resolved_weight, missing = 0.0, 0
    for i, shipment_id in enumerate(manifest["shipment_ids"], start=1): # Manifest order
        shipment = shipments.get(shipment_id)
        if not shipment:
            print(f"{i}. {shipment_id} | MISSING RECORD")
            missing += 1
            continue
        resolved_weight += shipment["weight_kg"]
        cargo_type = shipment.get("cargo_type") or "NOT PROVIDED" # Optional field, may be absent or null
        print(f"{i}. {shipment_id} | {shipment['customer']} | {shipment['weight_kg']} kg | {cargo_type}")

    print(f"Declared shipments: {len(manifest['shipment_ids'])}")
    print(f"Resolved weight: {resolved_weight:.2f} kg")
    print(f"Missing shipment records: {missing}")
    return call

    

def main():
    service = menu()
    while service != 10:
        #TODO: IMPORTANT: at the end lick all the tasks 
        if service == 1:
            #put the thing you need to run task 1 
            print()
        elif service == 2:
            inspect_manifest()
            print()
            main()

        elif service == 3:
            input_call_id = task_3.processing_call_id()
            shipment_ids = task_3.checking_call_id(input_call_id)

            if shipment_ids is not None:
                task_3.shipment_data(shipment_ids)
            print()
            main()

        elif service == 4:
            #put the thing you need to run task 1 
            print()

        elif service == 5:
            user_month = task_5.processing_user_month()
            task_5.checking_user_month(user_month)
            print()
            main()

    print("Console closed. HarborFlow operational data remains safe. ")
    


if __name__ == "__main__":
    main()
