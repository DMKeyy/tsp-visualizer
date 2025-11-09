
import random
import math
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def simulatedAnnealing(villes, distance_matrix,temperature, cooling_rate, max_iterations, visual=True):

    route = [0] + random.sample(range(1, len(villes)), len(villes) - 1) + [0]
    current_distance = Ville.calc_route_distance(route, distance_matrix)
    best_distance = current_distance

    best_route = route.copy()

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(8, 6))

    T = temperature
    i=0

    while True :

        i1, i2 = random.sample(range(1, len(route) - 1), 2)

        neighbor = route.copy()
        neighbor[i1], neighbor[i2] = neighbor[i2], neighbor[i1]

        neighbor_distance = Ville.calc_route_distance(neighbor, distance_matrix)

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

        if visual and plt_handle is not None:
            title = f"Iteration {i+1}/{max_iterations} | T={T:.5f} | Δ={delta_distance:.2f} | Best={best_distance:.2f} km"
            update_live_plot(villes, current_line, best_line, route, best_route, ax, title=title)

        if visual and plt_handle is not None:
            finalize_live_plot(plt_handle)

        i += 1

    return best_route, best_distance