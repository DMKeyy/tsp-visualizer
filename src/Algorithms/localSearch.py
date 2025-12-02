import random
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def localSearch(villes, distance_matrix, max_iterations, radius=2, visual=False):

    n = len(villes)
    if n < 3:
        route = [0, 0] if n == 1 else [0, 1, 0]
        return route, Ville.calc_route_distance(route, distance_matrix)

    route = [0] + random.sample(range(1, n), n - 1) + [0]
    current_distance = Ville.calc_route_distance(route, distance_matrix)
    best_route = route.copy()
    best_distance = current_distance

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(8, 6))

    iteration = 0
    for i in range(max_iterations):

        neighbors = []
        
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                neighbor = route.copy()
                neighbor[i:j+1] = neighbor[i:j+1][::-1]
                neighbors.append(neighbor)

        best_neighbor = None
        best_neighbor_distance = float('inf')
        for nb in neighbors:
            d = Ville.calc_route_distance(nb, distance_matrix)
            if d < best_neighbor_distance:
                best_neighbor_distance = d
                best_neighbor = nb

        if best_neighbor_distance < current_distance:
            route = best_neighbor.copy()
            current_distance = best_neighbor_distance

            if current_distance < best_distance:
                best_route = route.copy()
                best_distance = current_distance

            if visual and plt_handle is not None:
                i+=1
                title = f"Iteration {iteration} | Current = {current_distance:.2f} km | Best = {best_distance:.2f} km"
                update_live_plot(villes, current_line, best_line, route, best_route, ax, title=title)
            continue

    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)

    return best_route, best_distance
