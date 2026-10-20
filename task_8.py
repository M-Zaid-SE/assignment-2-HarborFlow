import data_access
from datetime import datetime  # used to turn date strings into real date objects we can compare


def weather_report():
    # Load the data. The _ ignores the skipped-rows/files count that each query returns.
    weather, _ = data_access.query_csv("weather")
    port_calls, _ = data_access.query_csv("port_calls")
    vessels, _ = data_access.query_json("vessels")

    vessel_name = input("Name of the vessel: ")

    vessel_id = None   # will hold the matching vessel's ID once found

    checker = True     # stays True if no vessel matches (used for the "not found" check below)

    # .lower().strip() makes the comparison ignore capitals and extra spaces
    for vessel in vessels:
        if vessel_name.lower().strip() == vessels[vessel].get("name").lower().strip():
            checker = False   # a match exists, so the vessel was found

        # Same comparison again; this time save the ID and stop searching
        if vessels[vessel].get("name").lower().strip() == vessel_name.lower().strip():
            vessel_id = vessels[vessel].get("vessel_id")
            break

    # No match found, so tell the user and leave the function
    if checker:
        print("Vessel not found.")
        return

    while True:
        date = input("Enter a date (YYYY-MM-DD): ")

        try:
            # strptime converts the text into a datetime using the given format;
            # .date() keeps only the date part. Wrong format raises ValueError.
            date = datetime.strptime(date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Error - Date must use YYYY-MM-DD.")

    counter = 0   # counts how many weather reports were printed

    for ports in port_calls:
        recommendation = []   # reset the recommendations for each port call
        if ports.get("vessel_id") == vessel_id:
            try:
                # Convert the call's arrival date text into a date so it can be compared
                arrival_date = datetime.strptime(ports["arrival_date"], "%Y-%m-%d").date()

                # Only keep calls on or after the date the user entered
                if arrival_date >= date:
                    for forecast in weather:
                        if forecast["date"] == str(arrival_date) and forecast["port_code"] == ports["port_code"]:
                            wind = forecast["wind_kmh"]
                            rain = forecast["precipitation_mm"]
                            waves = forecast["wave_height_m"]

                            if float(wind) >= 45:
                                recommendation.append("Suspend crane operations.")
                            if float(waves) >= 2.5:
                                recommendation.append("Arrange tug assistance.")
                            if float(rain) >= 8 and float(wind) < 45:
                                recommendation.append("Prepare covered handling.")
                            # Nothing triggered, so use the default plan
                            if not recommendation:
                                recommendation.append("Normal operating plan.")

                            print(f"\n ----------------------------------------------------")
                            print(f"{vessel_name.capitalize()}  |  {ports['port_code']}  |  {arrival_date}")
                            print(f"Wind: {wind} km/h  |  Rain: {rain} mm  |  Waves: {waves} m")
                            # ' '.join joins the list of recommendations into one line separated by spaces
                            print(f"Recommendations: {' '.join(recommendation)}")
                            counter += 1

                    if counter == 0:
                        print(f"Forecast unavailable.")
            # Raised if a port call's arrival_date or a weather value can't be converted
            except ValueError:
                print("Invalid date")

    return