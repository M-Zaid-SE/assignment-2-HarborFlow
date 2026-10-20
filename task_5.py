from pathlib import Path
import csv
import data_access


def processing_user_month():
    user_month = input("Enter a month as an integer from 1 to 12: ")

    while True:

        try:
            user_month = int(user_month)
        except ValueError:
            user_month = "Error"

        if user_month == "Error" or user_month > 12 or user_month < 1:
            print("Error - Enter a month from 1 to 12.")
            user_month = input("Enter a month as an integer from 1 to 12: ")
        else: return user_month

def load_vessels():
    vessels = {}
    vessel_records, _ = data_access.query_json("vessels")  #shared loader reports and skips malformed files
    for vid, vessel_data in vessel_records.items():
        vessels[vid] = vessel_data["name"]

    return vessels


def checking_user_month(user_month):
    vessel = load_vessels()
    port_call_path = Path("dataset/port_calls.csv")


    matching_calls = []

    with open(port_call_path, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)        #make the rows in the port_call.csv as dictionaryies
         
        for row in reader:
            arrival_date = row["arrival_date"]
            parts = arrival_date.split("-")  #splits the data in to year mm dd
            
            row_month = int(parts[1])
            if row_month == user_month:
                v_id = row["vessel_id"]      
                if v_id not in vessel:       #this checks if the vessel id from the matched row in the vessels folder
                    print(f"Skipping call with unknown vessel ID: {v_id}")
                else:
                    row["vessel_name"] = vessel[v_id]    #this addes a new key which is vessel name and a value as the name in the row
                    matching_calls.append(row)

              
        if not matching_calls:               #this checks if the matching_calls list is empty then it: therefore no matches
            print("No port calls found.")  
            return

        months_of_year = {"01":"January", "02" : "Febrary", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}
        row_month = f"{user_month:02d}"
        row_month = months_of_year[row_month]
        #month_name = months_of_year.get(row_month, "")
        print(f"Port calls in {row_month}:") 
        for match in matching_calls:
            call_id = match["call_id"]
            port_code = match["port_code"]
            vessel_name = match["vessel_name"]
            arrival_date = match["arrival_date"]
            parts = arrival_date.split("-")  #splits the data in to year mm dd
            row_year = parts[0]
            row_day = parts[2]
            #row_month = int(parts[1])
            #repeated
            months_of_year = {"01":"January", "02" : "Febrary", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}
            row_month = f"{user_month:02d}"
            row_month = months_of_year[row_month]
            #month_name = months_of_year.get(row_month, "")
            
            print(f"- {row_day} {row_month} {row_year} | {vessel_name} | {port_code} | {call_id}")

               
"""    
user_month = processing_user_month()
checking_user_month(user_month)


"""