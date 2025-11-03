import pandas as pd

from src.Ville import Ville


class TspSolver:
    def __init__(self, csvpath):
        self.data = pd.read_csv(csvpath)
        
        self.villes = []
        for index, row in self.data.iterrows():
            self.villes.append(Ville(row['city'], row['x_km'], row['y_km']))


        
    def get_villes(self):
        return self.villes

    
