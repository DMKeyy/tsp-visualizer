import random
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot



def hillClimbing(villes, distance_matrix, max_iterations, visual=True):
    route = [0] + random.sample(range(1, len(villes)), len(villes) - 1) + [0]
    best_distance = Ville.calc_route_distance(route, distance_matrix)

    best_route = route.copy()

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(8, 6))

    for i in range(max_iterations):

        i1, i2 = random.sample(range(1, len(route) - 1), 2)

        neighbor = route.copy()
        neighbor[i1], neighbor[i2] = neighbor[i2], neighbor[i1]

        neighbor_distance = Ville.calc_route_distance(neighbor, distance_matrix)

        if neighbor_distance < best_distance:
            best_route = neighbor.copy()
            best_distance = neighbor_distance
            route = neighbor.copy()

        if visual:
            title = f"Iteration {i+1}/{max_iterations} | Current = {neighbor_distance:.2f} km | Best = {best_distance:.2f} km"
            update_live_plot(villes, current_line, best_line, neighbor, best_route, ax, title=title)

    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)


    return best_route,best_distance

