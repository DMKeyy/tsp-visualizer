import random
import matplotlib.pyplot as plt
from src.Ville import Ville



def localSearch(villes, max_iterations):
    route = [0] + random.sample(range(1, len(villes)), len(villes) - 1) + [0]
    best_distance = Ville.calc_route_distance(route,villes)

    best_route = route.copy()

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    x_cities = [v.x for v in villes]
    y_cities = [v.y for v in villes]

    ax.scatter(x_cities, y_cities, color='royalblue', s=60, zorder=3)
    for v in villes:
        ax.text(v.x + 10, v.y + 10, v.name, fontsize=8)


    current_line, = ax.plot([], [], color='skyblue', linewidth=1.5, label='Current Route')
    best_line, = ax.plot([], [], color='orange', linewidth=2.5, label='Best Route')

    for i in range(max_iterations):

        i1, i2 = random.sample(range(1, len(route) - 1), 2)

        neighbor = route.copy()
        neighbor[i1], neighbor[i2] = neighbor[i2], neighbor[i1]

        neighbor_distance = Ville.calc_route_distance(neighbor, villes)

        if neighbor_distance < best_distance:
            best_route = neighbor.copy()
            best_distance = neighbor_distance
            route = neighbor.copy()

        x = [villes[j].x for j in neighbor]
        y = [villes[j].y for j in neighbor]
        current_line.set_data(x, y)


        if best_route:
            x_best = [villes[j].x for j in best_route]
            y_best = [villes[j].y for j in best_route]
            best_line.set_data(x_best, y_best)

        ax.set_title(f"Iteration {i+1}/{max_iterations} | Current = {neighbor_distance:.2f} km | Best = {best_distance:.2f} km")
        plt.pause(0.001)

    plt.ioff()
    plt.show(block=False)


    return best_route,best_distance

