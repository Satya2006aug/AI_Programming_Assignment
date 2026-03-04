import csv

class SimpleReflexAQIAgent:

    def __init__(self):

        self.vehicle_capacity = {
            "Cars": 6000,
            "Bikes": 3000,
            "Buses": 800,
            "Trucks": 1200
        }

        # Breakpoints for PM2.5 (CPCB)
        self.pm25_bp = [
            (0,30,0,50),
            (31,60,51,100),
            (61,90,101,200),
            (91,120,201,300),
            (121,250,301,400),
            (251,500,401,500)
        ]


    def read_environment(self, filename):

        data = []

        with open(filename,"r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["City"] == "Hyderabad":
                    data.append(row)

        return data


    def calculate_subindex(self, conc, breakpoints):

        conc = float(conc)

        for bp_lo, bp_hi, aqi_lo, aqi_hi in breakpoints:

            if bp_lo <= conc <= bp_hi:

                aqi = ((aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (conc - bp_lo) + aqi_lo
                return aqi

        return 0


    def compute_aqi(self, row):

        sub_indices = []

        if row["PM2.5"] != "":
            pm25_aqi = self.calculate_subindex(row["PM2.5"], self.pm25_bp)
            sub_indices.append(pm25_aqi)

        if len(sub_indices) == 0:
            return None

        return round(max(sub_indices))


    def decide_vehicles(self, aqi):

        if aqi <= 100:
            factor = 1
        elif aqi <= 200:
            factor = 0.75
        elif aqi <= 300:
            factor = 0.5
        elif aqi <= 400:
            factor = 0.25
        else:
            factor = 0.1

        allowed = {}

        for v in self.vehicle_capacity:
            allowed[v] = int(self.vehicle_capacity[v] * factor)

        return allowed


    def run(self, filename):

        env_data = self.read_environment(filename)

        dates = [row["Date"] for row in env_data if row["Date"] != ""]
        dates.sort()

        print("Hyderabad AQI data available from", dates[0], "to", dates[-1])

        user_date = input("Enter date (YYYY-MM-DD): ")

        for row in env_data:

            if row["Date"] == user_date:

                aqi = self.compute_aqi(row)

                if aqi is None:
                    print("No pollutant data available.")
                    return

                vehicles = self.decide_vehicles(aqi)

                print("\nAQI for Hyderabad on", user_date)
                print("Calculated AQI:", aqi)

                print("\nAllowed Vehicles:")

                for v in vehicles:
                    print(v, ":", vehicles[v])

                return

        print("No data found for that date.")


agent = SimpleReflexAQIAgent()
agent.run("city_day.csv")
