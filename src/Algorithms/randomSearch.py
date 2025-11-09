import random 
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def randomSearch(villes, distance_matrix,limit,visual=True):
    route = []
    best_route = None

    best_distance = float('inf')
    current_distance = 0

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(8, 6))

    for i in range(limit):
        middle_part = random.sample(range(1, len(villes)), len(villes) - 1)
        route = [0] + middle_part + [0]
        current_distance = Ville.calc_route_distance(route,distance_matrix)

        if current_distance < best_distance:
            best_distance = current_distance
            best_route = route 
        
        if visual:
            title = f"Iteration {i+1}/{limit} | Current = {current_distance:.2f} km | Best = {best_distance:.2f} km"
            update_live_plot(villes, current_line, best_line, route, best_route, ax, title=title)

    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)

    return best_route,best_distance

