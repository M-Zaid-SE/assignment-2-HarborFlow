#Menu bar 

def menu(): #prints the choices and takes input
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

def main():
    service = menu()
    while service != 10:
        if service == 1:
            #the function that runs task1
            print()
        elif service == 2:
            print()

        #IMPORTANT: at the end add all the choices
    
    print("Console closed. HarborFlow operational data remains safe. ")

if __name__ == "__main__":
    main()