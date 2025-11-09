import numpy as np

class Ville:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def calc_distance(start, end):
        return float(np.sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2))
    
    def calc_route_distance(route, distance_matrix):
        return sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))

