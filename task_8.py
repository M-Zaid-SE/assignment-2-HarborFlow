import data_access
from datetime import datetime


def weather_report():
    weather, _ = data_access.query_csv("weather")
    port_calls, _ = data_access.query_csv("port_calls")

    vessels, _ = data_access.query_json("vessels")

    vessel_name = input("Name of the vessel: ")

    vessel_id = None

    checker = True

    for vessel in vessels:
        if vessel_name.lower().strip() == vessels[vessel].get("name").lower().strip():
            checker = False

        if vessels[vessel].get("name").lower().strip() == vessel_name.lower().strip():
            vessel_id = vessels[vessel].get("vessel_id")
            break

    if checker:
        print("Vessel not found.")
        return

    while True:
        date = input("Enter a date (YYYY-MM-DD): ")

        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Error - Date must use YYYY-MM-DD.")

    future_dates = []
    port_codes = []
    call_ids = []

    counter = 0
    for ports in port_calls:
        recommendation = []
        if ports.get("vessel_id") == vessel_id:
            try:
                arrival_date = datetime.strptime(ports["arrival_date"], "%Y-%m-%d").date()
                if arrival_date >= date:
                    future_dates.append(ports["arrival_date"])
                    port_codes.append(ports["port_code"])
                    call_ids.append(ports["call_id"])

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
                            if not recommendation:
                                recommendation.append("Normal operating plan.")
                            print(f"\n ----------------------------------------------------")
                            print(f"{vessel_name.capitalize()}  |  {ports["port_code"]}  |  {arrival_date}")
                            print(f"Wind: {wind} km/h  |  Rain: {rain} mm  |  Waves: {waves} m")
                            print(f"Recommendations: {" ".join(recommendation)}")
                            counter += 1

                    if counter == 0:
                        print(f"No upcoming port calls found.")
            except ValueError:
                print("Invalid date")
    