import random
from copy import deepcopy
from src.Ville import Ville
from src.Utils.visualize import setup_live_plot, update_live_plot, finalize_live_plot


def geneticSearch( villes, distance_matrix, population_size=100, generations=500, mutation_rate=0.02, crossover_rate=0.8, elite_fraction=0.05, tournament_k=5, visual=False, plot_every=1):
    """
    Genetic Algorithm for TSP with Order Crossover (OX), tournament selection, swap mutation,
    and elitism. Uses distance_matrix for fast distance eval.
    Returns: best_route, best_distance
    """

    n = len(villes)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0, 0], 0.0
    if n == 2:
        route = [0, 1, 0]
        return route, Ville.calc_route_distance(route, distance_matrix)

    # --- Helpers ------------------------------------------------------------
    def create_random_route():
        return [0] + random.sample(range(1, n), n - 1) + [0]

    def route_distance(route):
        return Ville.calc_route_distance(route, distance_matrix)

    def fitness_from_distance(dist):
        # Avoid division by zero
        return 1.0 / (dist + 1e-9)

    def evaluate_population(pop):
        distances = [route_distance(ind) for ind in pop]
        fitnesses = [fitness_from_distance(d) for d in distances]
        return distances, fitnesses

    def tournament_selection(pop, fitnesses, k):
        """Return one selected individual (deepcopy) using tournament selection."""
        selected_idx = random.sample(range(len(pop)), k)
        best_idx = max(selected_idx, key=lambda i: fitnesses[i])
        return deepcopy(pop[best_idx])

    def ordered_crossover(parent1, parent2):
        """Order Crossover (OX) for permutations keeping start/end 0."""
        # parents are lists with 0 at start and end
        size = len(parent1)
        # working on the inner part (exclude first and last)
        start, end = sorted(random.sample(range(1, size - 1), 2))
        child_mid = parent1[start:end]
        # remaining from parent2 in order, skipping genes in child_mid
        p2_inner = [g for g in parent2[1:-1] if g not in child_mid]
        child_inner = p2_inner[:start - 1] + child_mid + p2_inner[start - 1:]
        child = [0] + child_inner + [0]
        return child

    def mutate_swap(route, mrate):
        """Swap mutation on inner genes (not the fixed 0 at ends)."""
        r = route.copy()
        for i in range(1, len(r) - 1):
            if random.random() < mrate:
                j = random.randint(1, len(r) - 2)
                r[i], r[j] = r[j], r[i]
        return r

    # --- Initialization -----------------------------------------------------
    population = [create_random_route() for _ in range(population_size)]
    distances, fitnesses = evaluate_population(population)

    # track global best
    best_idx = min(range(len(distances)), key=lambda i: distances[i])
    best_route = deepcopy(population[best_idx])
    best_distance = distances[best_idx]

    # visualization setup
    plt_handle = None
    current_line = best_line = None
    if visual:
        plt_handle, fig, ax, current_line, best_line = setup_live_plot(villes, figsize=(10, 8))

    elite_size = max(1, int(population_size * elite_fraction))

    # --- Main GA loop ------------------------------------------------------
    for gen in range(1, generations + 1):
        new_population = []

        # --- Elitism: keep top elites directly ------------------------------
        ranked = sorted(zip(population, distances), key=lambda x: x[1])
        elites = [deepcopy(r[0]) for r in ranked[:elite_size]]
        new_population.extend(elites)

        # --- Fill the rest of new_population -------------------------------
        while len(new_population) < population_size:
            # Selection
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)

            # Crossover (with probability)
            if random.random() < crossover_rate:
                child = ordered_crossover(parent1, parent2)
            else:
                # no crossover -> clone one parent
                child = deepcopy(parent1)

            # Mutation
            child = mutate_swap(child, mutation_rate)

            # Ensure valid child (sanity)
            # child should be permutation of 0..n-1 with 0 at ends
            # (OX and swap preserve validity; this is a quick guard)
            if len(set(child[1:-1])) != n - 1:
                # fallback: random valid route
                child = create_random_route()

            new_population.append(child)

        # --- Replace population and evaluate --------------------------------
        population = new_population[:population_size]
        distances, fitnesses = evaluate_population(population)

        # update best
        gen_best_idx = min(range(len(distances)), key=lambda i: distances[i])
        gen_best_distance = distances[gen_best_idx]
        if gen_best_distance < best_distance:
            best_distance = gen_best_distance
            best_route = deepcopy(population[gen_best_idx])

        # --- Visualization update (every `plot_every` gens) -----------------
        if visual and (gen % plot_every == 0):
            title = f"Gen {gen}/{generations} | Best = {best_distance:.2f} km"
            # show current best route (population best) and global best
            update_live_plot(villes, current_line, best_line, population[gen_best_idx], best_route, ax, title=title)

    # finalize plot
    if visual and plt_handle is not None:
        finalize_live_plot(plt_handle)

    return best_route, best_distance
