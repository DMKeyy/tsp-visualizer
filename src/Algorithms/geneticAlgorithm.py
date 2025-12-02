import random
from copy import deepcopy
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def geneticSearch( villes, distance_matrix, population_size=100, generations=500, mutation_rate=0.02, crossover_rate=0.8, elite_fraction=0.1, tournament_k=5, visual=False, plot_every=1):

    n = len(villes)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0, 0], 0.0
    if n == 2:
        route = [0, 1, 0]
        return route, Ville.calc_route_distance(route, distance_matrix)

    def create_random_route():
        return [0] + random.sample(range(1, n), n - 1) + [0]

    def route_distance(route):
        return Ville.calc_route_distance(route, distance_matrix)

    def fitness_from_distance(dist):
        return 1.0 / (dist + 1e-9)

    def evaluate_population(population):
        distances = [route_distance(ind) for ind in population]
        fitnesses = [fitness_from_distance(d) for d in distances]
        return distances, fitnesses

    def tournament_selection(population, fitnesses, k):
        selected_idx = random.sample(range(len(population)), k)
        best_idx = max(selected_idx, key=lambda i: fitnesses[i])
        return deepcopy(population[best_idx])

    def ordered_crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(1, size - 1), 2))
        child_mid = parent1[start:end]
        p2_inner = [g for g in parent2[1:-1] if g not in child_mid]
        child_inner = p2_inner[:start - 1] + child_mid + p2_inner[start - 1:]
        child = [0] + child_inner + [0]
        return child

    def mutate_swap(route, mrate):
        r = route.copy()
        for i in range(1, len(r) - 1):
            if random.random() < mrate:
                j = random.randint(1, len(r) - 2)
                r[i], r[j] = r[j], r[i]
        return r


    population = [create_random_route() for _ in range(population_size)]
    distances, fitnesses = evaluate_population(population)

    best_idx = min(range(len(distances)), key=lambda i: distances[i])
    best_route = deepcopy(population[best_idx])
    best_distance = distances[best_idx]

    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(10, 8))

    elite_size = max(1, int(population_size * elite_fraction))

    for gen in range(1, generations + 1):
        new_population = []

        ranked = sorted(zip(population, distances), key=lambda x: x[1])
        elites = [deepcopy(r[0]) for r in ranked[:elite_size]]
        new_population.extend(elites)

        while len(new_population) < population_size:
            
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)

            if random.random() < crossover_rate:
                child = ordered_crossover(parent1, parent2)
            else:
                child = deepcopy(parent1)

            child = mutate_swap(child, mutation_rate)

            inner = child[1:-1]

            # Vérifier que toutes les villes sont présentes une seule fois
            if sorted(inner) != list(range(1, n)):
                missing = list(set(range(1, n)) - set(inner))

                index = 0
                for i in range(len(inner)):
                    if inner.count(inner[i]) > 1:
                        inner[i] = missing[index]
                        index += 1
                child = [0] + inner + [0]

            if len(set(child[1:-1])) != n - 1:
                child = create_random_route()

            new_population.append(child)

        population = new_population[:population_size]
        distances, fitnesses = evaluate_population(population)

        generation_best_index = min(range(len(distances)), key=lambda i: distances[i])
        gen_best_distance = distances[generation_best_index]
        if gen_best_distance < best_distance:
            best_distance = gen_best_distance
            best_route = deepcopy(population[generation_best_index])
        if visual and (gen % plot_every == 0):
            title = f"Gen {gen}/{generations} | Best = {best_distance:.2f} km"
            update_live_plot(villes, current_line, best_line, population[generation_best_index], best_route, ax, title=title)

    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)

    return best_route, best_distance
