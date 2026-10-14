from pathlib import Path
import json 

def processing_call_id():
    input_call_id = input("Enter caller ID: ")
    input_call_id = input_call_id.strip().upper() #strip removes the surrounding white space

    while (len(input_call_id) < 12 or 
           input_call_id[0:3] != "HFL" or 
           input_call_id[3] != "-" or 
           not input_call_id[4:7].isalpha() or 
           input_call_id[7] != "-" or 
           not input_call_id[8:].isdigit()):
        
        print("Wrong format for call ID: eg. HFL-abc-1234")
        input_call_id = input("Enter call ID: ").strip().upper()
        
    return input_call_id

def checking_call_id(input_call_id):
    # This ensures Python looks relative to the script's actual location
    
    calling_file = Path("dataset/manifests")

    # Loop through every JSON file in the folder
    for file_path in calling_file.glob("*.json"):                      #the * tells python to go through any or more 
        try:
            # Open and load the JSON file as a dictionary
            with open(file_path, "r", encoding="utf-8") as file:       #opens the file and reads through it 
                manifest = json.load(file)                             #go throgh each json file
            # Check if the dictionary's call_id matches the user's input 
            file_call_id = manifest.get("call_id", "").strip().upper()

            #checks if the caller id matches the input
            if file_call_id == input_call_id:
                print(f"Match found {file_path.name}")                 #the task doesn´t require it but lets the user know
                shipment_ids = manifest.get("shipment_ids", [])        #now we got the shipment ids
                return shipment_ids        
            
        except (FileNotFoundError, OSError, json.JSONDecodeError):     #this excepts the error and alows the user to see the actual problem
            print(f"Manifest unavailable: {file_path.name}")
            continue 
    print("Port call not found")                                       #if there is not match  
    return None #menu()  TRY To return to menu 

def shipment_data(shipment_ids):
    category = 0
    category_name = 0
    controled = 0
    Cold_chain = 0
    expedite = 0
    STANDARD = 0
    for shipment in shipment_ids:                                      #goes through every shipment linked to the users caller id 
        second_call_to_file = Path("dataset/shipments")

        for file_path_2 in second_call_to_file.glob("*.json"):         #.glob() is used to find files and folders whose names match a pattern
            
            with open(file_path_2, "r", encoding="utf-8") as file:
                shipment_id = json.load(file)
            second_call_to_file = shipment_id.get("shipment_id", "").strip().upper()

            if second_call_to_file == shipment:
                hazardous = shipment_id.get("hazardous", "")            #can not strip() or upper() to bool or float
                temperature_controlled = shipment_id.get("temperature_controlled", "")
                priority = shipment_id.get("priority", "").strip().upper()
                weight_kg = shipment_id.get("weight_kg", "")

                #First matching condition from assignment
                if hazardous == True:
                    category = "CONTROLLED"
                    category_name = "Hazardous cargo"
                    controled += 1
                elif temperature_controlled == True:
                    category = "COLD CHAIN"
                    category_name = "Temp controled"
                    Cold_chain += 1
                elif priority == "EXPRESS" or weight_kg >= 5000:
                    category = "EXPEDITE"
                    category_name = "Express service"
                    expedite += 1
                else:
                    category = "STANDARD"
                    category_name = "Standary service"
                    STANDARD += 1
                
            continue

        print(f"{shipment} | {category} | {category_name}")             #prints for every shipment
    #only prints after everything
    print(f"Category totals: CONTROLLED = {controled}, COLD CHAIN = {Cold_chain}, EXPEDITE = {expedite}, STANDARD = {STANDARD}")
  




input_call_id = processing_call_id()
shipment_ids = checking_call_id(input_call_id)

if shipment_ids is not None:
    shipment_data(shipment_ids)