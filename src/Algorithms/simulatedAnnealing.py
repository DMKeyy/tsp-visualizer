import random
import math
import matplotlib.pyplot as plt
from src.Ville import Ville


def simulatedAnnealing(villes, temperature, cooling_rate, max_iterations, visual=True):

    route = [0] + random.sample(range(1, len(villes)), len(villes) - 1) + [0]
    current_distance = Ville.calc_route_distance(route,villes)
    best_distance = current_distance

    best_route = route.copy()

    if visual:
        import matplotlib.pyplot as plt
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

        x_cities = [v.x for v in villes]
        y_cities = [v.y for v in villes]

        ax.scatter(x_cities, y_cities, color='royalblue', s=60, zorder=3)
        for v in villes:
            ax.text(v.x + 10, v.y + 10, v.name, fontsize=8)


        current_line, = ax.plot([], [], color='skyblue', linewidth=1.5, label='Current Route')
        best_line, = ax.plot([], [], color='orange', linewidth=2.5, label='Best Route')

    T = temperature

    for i in range(max_iterations):

        i1, i2 = random.sample(range(1, len(route) - 1), 2)

        neighbor = route.copy()
        neighbor[i1], neighbor[i2] = neighbor[i2], neighbor[i1]

        neighbor_distance = Ville.calc_route_distance(neighbor, villes)

        delta_distance = neighbor_distance - current_distance

        if delta_distance < 0 : 
            route = neighbor.copy()
            current_distance = neighbor_distance

            if neighbor_distance < best_distance:
                best_route = neighbor.copy()
                best_distance = neighbor_distance

        else:
            if random.uniform(0, 1) < math.exp(-delta_distance / T):
                route = neighbor.copy()
                current_distance = neighbor_distance


        T *= cooling_rate

        if T < 1e-6:
            break


        if visual:
            x = [villes[j].x for j in route]
            y = [villes[j].y for j in route]
            current_line.set_data(x, y)


            if best_route:
                x_best = [villes[j].x for j in best_route]
                y_best = [villes[j].y for j in best_route]
                best_line.set_data(x_best, y_best)

            ax.set_title(f"Iteration {i+1}/{max_iterations} | T={T:.5f} | Δ={delta_distance:.2f} | Best={best_distance:.2f} km")
            plt.pause(0.001)


    if visual:
        plt.ioff()
        plt.show(block=False)

    return best_route,best_distance