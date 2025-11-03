import numpy as np

class Ville:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def calc_distance(start, end):
        return float(np.sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2))
    
    def calc_route_distance(route, villes):
        distance = 0
        for i in range(len(route)-1):
            distance += Ville.calc_distance(villes[route[i]],villes[route[i+1]])

        return distance

    
