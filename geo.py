from geopy.distance import distance

from db import Database
from repository import Atm

# database
config_file = 'config.ini'
db = Database(config_file)
atm = Atm(db)

class Distance:

    def __init__(self, db):
        self.db = db

    def check_distance(self, longitude, latitude):
        all_atm_coordinates = atm.get_all_atm_coordinates()

        for coordinates in all_atm_coordinates: 
            dist = distance((latitude, longitude), (coordinates[1], coordinates[2])).m

            if dist <= 100:
                return coordinates[0]

        return '0'
    