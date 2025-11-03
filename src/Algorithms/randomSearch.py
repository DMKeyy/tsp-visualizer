import random 
from src.Ville import Ville
import matplotlib.pyplot as plt

def randomSearch(villes,limit):
    route = []
    best_route = None

    best_distance = float('inf')
    current_distance = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    x_cities = [v.x for v in villes]
    y_cities = [v.y for v in villes]

    ax.scatter(x_cities, y_cities, color='royalblue', s=60, zorder=3)
    for v in villes:
        ax.text(v.x + 10, v.y + 10, v.name, fontsize=8)


    current_line, = ax.plot([], [], color='skyblue', linewidth=1.5, label='Current Route')
    best_line, = ax.plot([], [], color='orange', linewidth=2.5, label='Best Route')
    

    for i in range(limit):
        middle_part = random.sample(range(1, len(villes)), len(villes) - 1)
        route = [0] + middle_part + [0]
        current_distance = Ville.calc_route_distance(route,villes)

        if current_distance < best_distance:
            best_distance = current_distance
            best_route = route 
        
        x = [villes[j].x for j in route]
        y = [villes[j].y for j in route]
        current_line.set_data(x, y)

        if best_route:
            x_best = [villes[j].x for j in best_route]
            y_best = [villes[j].y for j in best_route]
            best_line.set_data(x_best, y_best)

        ax.set_title(f"Iteration {i+1}/{limit} | Current = {current_distance:.2f} km | Best = {best_distance:.2f} km")
        plt.pause(0.001)

    plt.ioff()
    plt.show(block=False)

    return best_route,best_distance

