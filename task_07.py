from pathlib import Path
import json 
import task_3



def checking_call_id(input_call_id):
    
    
    calling_file = Path("dataset/manifests")

    
    for file_path in calling_file.glob("*.json"):                 
        try:
           
            with open(file_path, "r", encoding="utf-8") as file:      
                manifest = json.load(file)                        
            
            file_call_id = manifest.get("call_id", "").strip().upper()

            
            if file_call_id == input_call_id:
                print(f"Match found {file_path.name}")   
                #this whole function is taken from task 3 expect for this next 2 lines              
                event_codes = manifest.get("event_codes", [])      
                return event_codes        
            
        except (FileNotFoundError, OSError, json.JSONDecodeError):   
            print(f"Manifest unavailable: {file_path.name}")
            continue 
    print("Port call not found")                                     
    return None

def arranging_event_codes(event_codes):
    sequenced_event_codes = []

    for event in event_codes:
        if event not in sequenced_event_codes:
            sequenced_event_codes.append(event)
        else:
            index_of_event = sequenced_event_codes.index(event)
            old_event = sequenced_event_codes[index_of_event]
            sequenced_event_codes.remove(old_event)
            sequenced_event_codes.append(event)
            sequenced_event_codes = sequenced_event_codes[index_of_event:]


    y = ",".join(event_codes)
    print(f"Event codes: {y}")
    print(f"Longest stable sequence length: {len(sequenced_event_codes)}")
    x = " -> ".join(sequenced_event_codes)  #this turn the , in to -> in the list and removes the brackets
    print(f"Sequence: {x}")
    return


input_call_id = task_3.processing_call_id()
event_codes = checking_call_id(input_call_id)
arranging_event_codes(event_codes)