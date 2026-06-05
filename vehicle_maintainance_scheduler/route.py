from utils import *
from service import VehicleService


vehicle_data = get_vehicles_data()
depots_data = get_depots_data()
print(VehicleService.compute_overall(vehicles_data=vehicle_data, depots_data=depots_data))
print(VehicleService.computer_per_depo(vehicles_data=vehicle_data, depots_data=depots_data))
