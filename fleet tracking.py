import pandas as pd
import numpy as np

# Read input files
demand = pd.read_csv('E:/shall hack/demand.csv')
vehicles = pd.read_csv('E:/shall hack/vehicles.csv')
vehicles_fuels = pd.read_csv('E:/shall hack/vehicles_fuels.csv')
fuels = pd.read_csv('E:/shall hack/fuels.csv')
carbon_emissions = pd.read_csv('E:/shall hack/carbon_emissions.csv')

# Initialize variables
solution = []
fleet = {}  # Keeps track of the current fleet composition

# Function to add an entry to the solution
def add_to_solution(year, vehicle_id, num_vehicles, operation, fuel, distance_bucket, distance_per_vehicle):
    solution.append({
        'Year': year,
        'ID': vehicle_id,
        'Num_Vehicles': num_vehicles,
        'Type': operation,
        'Fuel': fuel,
        'Distance_bucket': distance_bucket,
        'Distance_per_vehicle(km)': distance_per_vehicle
    })

# Function to buy vehicles
def buy_vehicles(year):
    new_vehicles = vehicles[vehicles['Year'] == year]
    for _, row in new_vehicles.iterrows():
        vehicle_id = row['ID']
        size_bucket = row['Size']
        distance_bucket = row['Distance']
        fuel_type = vehicles_fuels[vehicles_fuels['ID'] == vehicle_id]['Fuel'].values[0]
        num_vehicles = 1  # Example: buy 1 of each vehicle type per year
        add_to_solution(year, vehicle_id, num_vehicles, 'Buy', fuel_type, distance_bucket, 0)
        if vehicle_id not in fleet:
            fleet[vehicle_id] = 0
        fleet[vehicle_id] += num_vehicles

# Function to use vehicles to meet demand
def use_vehicles(year):
    yearly_demand = demand[demand['Year'] == year]
    for _, row in yearly_demand.iterrows():
        size_bucket = row['Size']
        distance_bucket = row['Distance']
        demand_km = row['Demand (km)']
        
        # Example: Allocate demand equally among all vehicles of the right type
        available_vehicles = [v for v in fleet.keys() if size_bucket in v and distance_bucket in v]
        num_vehicles = len(available_vehicles)
        if num_vehicles > 0:
            distance_per_vehicle = demand_km / num_vehicles
            for vehicle_id in available_vehicles:
                fuel_type = vehicles_fuels[vehicles_fuels['ID'] == vehicle_id]['Fuel'].values[0]
                add_to_solution(year, vehicle_id, fleet[vehicle_id], 'Use', fuel_type, distance_bucket, distance_per_vehicle)

# Function to sell old vehicles
def sell_old_vehicles(year):
    if year >= 2033:  # Vehicles bought in 2023 should be sold in 2033
        old_vehicles = vehicles[vehicles['Year'] == year - 10]
        for _, row in old_vehicles.iterrows():
            vehicle_id = row['ID']
            if vehicle_id in fleet:
                num_vehicles = fleet[vehicle_id]
                sell_vehicles = int(num_vehicles * 0.2)  # Example: sell 20% of each vehicle type
                if sell_vehicles > 0:
                    add_to_solution(year, vehicle_id, sell_vehicles, 'Sell', vehicles_fuels[vehicles_fuels['ID'] == vehicle_id]['Fuel'].values[0], row['Distance'], 0)
                    fleet[vehicle_id] -= sell_vehicles

# Process each year
for year in range(2023, 2039):
    buy_vehicles(year)
    use_vehicles(year)
    sell_old_vehicles(year)

# Convert solution list to DataFrame
solution_df = pd.DataFrame(solution)

# Save the solution to a CSV file
solution_df.to_csv('E:/shall hack/solutionss.csv', index=False)
