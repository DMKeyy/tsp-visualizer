import pandas as pd

from src.Ville import Ville


class TspSolver:
    def __init__(self, csvpath):        
        self.villes = self.load_villes(csvpath)
        self.distance_matrix = self.calculate_distance_matrix()

    def load_villes(self, csvpath):
        data = pd.read_csv(csvpath)
        villes = []
        for index, row in data.iterrows():
            villes.append(Ville(row['city'], row['x_km'], row['y_km']))
        return villes
    
    def calculate_distance_matrix(self):
        size = len(self.villes)
        distance_matrix = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if i != j:
                    distance_matrix[i][j] = Ville.calc_distance(self.villes[i], self.villes[j])
        return distance_matrix

    def get_villes(self):
        return self.villes
    
    def get_distance_matrix(self):
        return self.distance_matrix

    
