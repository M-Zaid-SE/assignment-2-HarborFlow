# Imports
from datetime import datetime
import data_access
import task_3, task_4, task_5, task_6, task_8, task_9
# Constants


def parse_date(text):
    '''Takes a date string and returns a date object. Raises ValueError unless it is exactly YYYY-MM-DD'''
    if len(text) != 10: # strptime alone accepts short forms like 2026-10-1
        raise ValueError(f"'{text}' does not use YYYY-MM-DD")
    return datetime.strptime(text, "%Y-%m-%d").date()

# Task 1
def list_vessels():
    vessels, skipped_vessels = data_access.query_json("vessels")
    data_access.load_vessels(vessels, skipped_vessels)



# Task 2
def inspect_manifest(): 
    vessel_id, call_date = None, None

    vessels, skipped_vessels = data_access.query_json("vessels")
    port_calls, _ = data_access.query_csv("port_calls")

    data_access.load_vessels(vessels, skipped_vessels) # Display available vessels

    # Match name case-insensitively. Unknown vessel returns to menu.
    input_vessel = input("Vessel name: ").strip().casefold()
    for vid, vessel in vessels.items():
        if vessel_id is None and vessel["name"].casefold() == input_vessel: # Keep the first match
            vessel_id = vid

    if vessel_id is None:
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
        print(f"{i}. {shipment_id} | {shipment['customer']} | {float(shipment['weight_kg'])} kg | {cargo_type}")

    print(f"Declared shipments: {len(manifest['shipment_ids'])}")
    print(f"Resolved weight: {resolved_weight:.2f} kg")
    print(f"Missing shipment records: {missing}")
    return call



# Task 4
def export_customer_profile():
    name = input("Customer name: ").strip()
    found_in = task_4.match_name(name)
    if found_in == []:
        print("Customer not found.")
    else:
        task_4.check_file_exists()
        shipment_count_total, total_weight_kg, express_count, destinations, name = task_4.calculations(found_in)
        task_4.add_profile(name, shipment_count_total, total_weight_kg, express_count, destinations)
        print("Customer profile updated: exports/customer-profiles.csv")


def main():
    running = True # Loop-state variable, only option 10 turns it off

    while running:
        print("HARBORFLOW PORT INTELLIGENCE")
        print("1. List registered vessels")
        print("2. Inspect a vessel manifest")
        print("3. Identify priority cargo")
        print("4. Export a customer operations profile")
        print("5. Find port calls by month")
        print("6. Sanitize an incident report")
        print("7. Analyze the longest stable event sequence")
        print("8. Assess weather risk for upcoming calls")
        print("9. Search incident reports")
        print("10. Close console")

        service = 0 # Re-ask until the input is an integer from 1 to 10
        while service < 1 or service > 10:
            try:
                service = int(input("Select service: "))
            except ValueError:
                service = 0
            if service < 1 or service > 10:
                print("Error - Select a service from 1 to 10.")

        match service:
            case 1:
                list_vessels()
            case 2:
                inspect_manifest()
            case 3:
                input_call_id = task_3.processing_call_id()
                shipment_ids = task_3.checking_call_id(input_call_id)
                if shipment_ids is not None:
                    task_3.shipment_data(shipment_ids)
            case 4:
                export_customer_profile()
            case 5:
                user_month = task_5.processing_user_month()
                task_5.checking_user_month(user_month)
            case 6:
                chosen_incident = task_6.show_incidents()
                changed_mail, incident, copied_file = task_6.replacing_container_identifiers(chosen_incident)
                task_6.write_file(changed_mail, incident, copied_file)
            case 7:
                input_call_id = task_3.processing_call_id()
                manifests, _ = data_access.query_json("manifests")
                event_codes = None
                for call_id, manifest in manifests.items():
                    if call_id.strip().upper() == input_call_id:
                        event_codes = manifest["event_codes"]

                if event_codes is None:
                    print("Port call not found")
                else:
                    # Sliding window: start of the current window and last position of every event
                    start, best_start, best_length = 0, 0, 0
                    last_seen = {}
                    for position, event in enumerate(event_codes):
                        if event in last_seen and last_seen[event] >= start:
                            start = last_seen[event] + 1 # Move just beyond the previous occurrence
                        last_seen[event] = position
                        if position - start + 1 > best_length: # Strictly longer, so ties keep the first
                            best_start, best_length = start, position - start + 1

                    print("Event codes: " + ",".join(event_codes))
                    print("Longest stable sequence length: " + str(best_length))
                    print("Sequence: " + " -> ".join(event_codes[best_start:best_start + best_length]))
            case 8:
                task_8.weather_report()
            case 9:
                user_search = input("Search incident reports: ")
                task_9.search(user_search)
            case 10:
                running = False

        if running:
            print()

    print("Console closed. HarborFlow operational data remains safe.")


if __name__ == "__main__":
    main()
