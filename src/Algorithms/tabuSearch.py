import random
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def tabuSearch(villes, distance_matrix, max_iterations, tabu_size, neighborhood_size, visual=True):

    route = [0] + random.sample(range(1, len(villes)), len(villes) - 1) + [0]
    current_distance = Ville.calc_route_distance(route, distance_matrix)
    best_distance = current_distance

    best_route = route.copy()

    tabu_list = []

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(8, 6))


    for i in range(max_iterations):
        best_candidate = None
        best_candidate_distance = float('inf')
        best_move = None

        for _ in range(neighborhood_size):
            i1, i2 = random.sample(range(1, len(route) - 1), 2)
            neighbor = route.copy()
            neighbor[i1], neighbor[i2] = neighbor[i2], neighbor[i1]
            move = (i1, i2)

            if move in tabu_list:
                continue

            distance = Ville.calc_route_distance(neighbor, distance_matrix)

            if distance < best_candidate_distance:
                best_candidate = neighbor
                best_candidate_distance = distance
                best_move = move

        if best_candidate is not None:
            route = best_candidate
            current_distance = best_candidate_distance

            tabu_list.append(best_move)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            if current_distance < best_distance:
                best_route = route.copy()
                best_distance = current_distance


        if visual:
            title = (f"Iteration {i+1}/{max_iterations} | " f"Current = {current_distance:.2f} km | Best = {best_distance:.2f} km")
            update_live_plot(villes, current_line, best_line, route, best_route, ax, title=title)

    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)

    return best_route, best_distance
