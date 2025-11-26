from asyncio.log import logger
import tkinter as tk
from tkinter import ttk, messagebox
from src.TspSolver import TspSolver
from src.Algorithms.randomSearch import randomSearch
from src.Algorithms.localSearch import localSearch
from src.Algorithms.hillClimbing import hillClimbing
from src.Algorithms.simulatedAnnealing import simulatedAnnealing
from src.Algorithms.tabuSearch import tabuSearch
from src.Algorithms.geneticAlgorithm import geneticSearch

from src.Utils.Logger import Logger
from src.Utils.visualize import plot_average_distance, plot_best_distance, visualize_route
import time



path = "data/algeria_20_cities_xy.csv"
save_path = "data/results.csv"


def run_algorithm():
    algo = algo_choice.get()
    try:
        limit = int(iter_entry.get())
        if limit <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of iterations.")
        return

    solver = TspSolver(path)
    villes = solver.get_villes()
    visual = visual_var.get()
    distance_matrix = solver.get_distance_matrix()


    
    if algo == "Recherche aléatoire":
        best_route, best_distance = randomSearch(villes, distance_matrix, limit, visual=visual)
    elif algo == "Recherche Local":
            best_route, best_distance = localSearch(villes, distance_matrix, radius=2, visual=visual)
    elif algo == "Recherche Hill climbing":
        best_route, best_distance = hillClimbing(villes, distance_matrix, visual=visual)
    elif algo == "Recherche Recuit-Simulé":
        try:
            temperature = float(temp_entry.get())
            cooling_rate = float(cooling_entry.get())
            epsilon = float(epsilon_entry.get())
            if temperature <= 0:
                raise ValueError("Temperature must be > 0")
            if not (0 < cooling_rate < 1):
                raise ValueError("Cooling rate must be between 0 and 1 (exclusive)")
            if epsilon <= 0:
                raise ValueError("Epsilon must be > 0")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid simulated annealing parameters: {e}")
            return
            
        best_route, best_distance = simulatedAnnealing(villes, distance_matrix, temperature, cooling_rate, epsilon, visual=visual)

    elif algo == "Recherche Tabu":
        tabu_size = 15
        neighborhood_size = 100
        best_route, best_distance = tabuSearch(villes, distance_matrix, limit, tabu_size, neighborhood_size, visual=visual)
    elif algo == "Recherche par Algorithme génétique":
        try:
            pop_size = int(pop_size_entry.get())
            gens = int(generations_entry.get())
            mut_rate = float(mutation_entry.get())
            cross_rate = float(crossover_entry.get())
            if pop_size <= 0:
                raise ValueError("Population size must be > 0")
            if gens <= 0:
                raise ValueError("Generations must be > 0")
            if not (0 <= mut_rate <= 1):
                raise ValueError("Mutation rate must be between 0 and 1")
            if not (0 <= cross_rate <= 1):
                raise ValueError("Crossover rate must be between 0 and 1")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid genetic algorithm parameters: {e}")
            return
        
        best_route, best_distance = geneticSearch(
            villes, distance_matrix, 
            population_size=pop_size, 
            generations=gens,
            mutation_rate=mut_rate, 
            crossover_rate=cross_rate,
            visual=visual
        )
    else:
        messagebox.showinfo("Info", "Selected algorithm not available yet.")
        return
    
    if not visual:
        visualize_route(villes, best_route, title=f"Best Route - {algo} ({best_distance:.2f} km)")

    route_names = " → ".join([villes[i].name for i in best_route])
    messagebox.showinfo("Result", f"{algo} Finished!\n\n"f"Best Distance: {best_distance:.2f} km\n\n"f"Best Route:\n{route_names}")
    
    logger.record(algo, best_distance, best_route, limit)
    logger.save_csv(save_path)

def show_results():
    avg_series = logger.get_avg_per_algo(save_path)
    best_series = logger.get_best_per_algo(save_path)
    
    plot_average_distance(avg_series)
    plot_best_distance(best_series)
    

root = tk.Tk()
root.title("TSP Solver")
root.geometry("380x520")
root.resizable(False, False)

logger = Logger()

tk.Label(root, text="TSP Solver", font=("Arial", 18, "bold")).pack(pady=10)


tk.Label(root, text="Choose an algorithm:", font=("Arial", 12)).pack(pady=(10, 5))
algo_choice = ttk.Combobox(root, values=["Recherche aléatoire","Recherche Local" ,"Recherche Hill climbing", "Recherche Recuit-Simulé","Recherche Tabu","Recherche par Algorithme génétique"],state="readonly", font=("Arial", 12))
algo_choice.current(0)
algo_choice.pack(pady=5)


iter_label = tk.Label(root, text="Number of iterations:", font=("Arial", 12))
iter_label.pack(pady=(10, 5))
iter_entry = tk.Entry(root, font=("Arial", 12), justify="center")
iter_entry.insert(0, "5000")
iter_entry.pack(pady=5)

visual_var = tk.BooleanVar(value=True)
visual_check = tk.Checkbutton(root, text="Show Visualization", variable=visual_var, font=("Arial", 10))
visual_check.pack(pady=(4, 8))

temp_label = tk.Label(root, text="Initial Temperature:", font=("Arial", 12))
temp_entry = tk.Entry(root, font=("Arial", 12), justify="center")
temp_entry.insert(0, "1000")

cooling_label = tk.Label(root, text="Cooling Rate (0-1):", font=("Arial", 12))
cooling_entry = tk.Entry(root, font=("Arial", 12), justify="center")
cooling_entry.insert(0, "0.9985")

epsilon_label = tk.Label(root, text="Epsilon (stopping threshold):", font=("Arial", 12))
epsilon_entry = tk.Entry(root, font=("Arial", 12), justify="center")
epsilon_entry.insert(0, "0.01")

pop_size_label = tk.Label(root, text="Population Size:", font=("Arial", 12))
pop_size_entry = tk.Entry(root, font=("Arial", 12), justify="center")
pop_size_entry.insert(0, "1000")

generations_label = tk.Label(root, text="Generations:", font=("Arial", 12))
generations_entry = tk.Entry(root, font=("Arial", 12), justify="center")
generations_entry.insert(0, "500")

mutation_label = tk.Label(root, text="Mutation Rate (0-1):", font=("Arial", 12))
mutation_entry = tk.Entry(root, font=("Arial", 12), justify="center")
mutation_entry.insert(0, "0.02")

crossover_label = tk.Label(root, text="Crossover Rate (0-1):", font=("Arial", 12))
crossover_entry = tk.Entry(root, font=("Arial", 12), justify="center")
crossover_entry.insert(0, "0.8")

def show_or_hide_sa_fields(event=None):
    # Show/hide Simulated Annealing specific inputs
    if algo_choice.get() == "Recherche Recuit-Simulé":
        temp_label.pack(pady=(8, 2))
        temp_entry.pack(pady=2)
        cooling_label.pack(pady=(8, 2))
        cooling_entry.pack(pady=2)
        epsilon_label.pack(pady=(8, 2))
        epsilon_entry.pack(pady=2)
    else:
        temp_label.pack_forget()
        temp_entry.pack_forget()
        cooling_label.pack_forget()
        cooling_entry.pack_forget()
        epsilon_label.pack_forget()
        epsilon_entry.pack_forget()

    # Show/hide Genetic Algorithm specific inputs
    if algo_choice.get() == "Recherche par Algorithme génétique":
        pop_size_label.pack(pady=(8, 2))
        pop_size_entry.pack(pady=2)
        generations_label.pack(pady=(8, 2))
        generations_entry.pack(pady=2)
        mutation_label.pack(pady=(8, 2))
        mutation_entry.pack(pady=2)
        crossover_label.pack(pady=(8, 2))
        crossover_entry.pack(pady=2)
    else:
        pop_size_label.pack_forget()
        pop_size_entry.pack_forget()
        generations_label.pack_forget()
        generations_entry.pack_forget()
        mutation_label.pack_forget()
        mutation_entry.pack_forget()
        crossover_label.pack_forget()
        crossover_entry.pack_forget()

    # Show iterations only for Random Search and Tabu Search
    if algo_choice.get() in ("Recherche aléatoire", "Recherche Tabu"):
        if not iter_label.winfo_ismapped():
            iter_label.pack(pady=(10, 5))
            iter_entry.pack(pady=5)
    else:
        iter_label.pack_forget()
        iter_entry.pack_forget()

algo_choice.bind("<<ComboboxSelected>>", show_or_hide_sa_fields)

show_or_hide_sa_fields()

tk.Button(root, text="Run Algorithm", font=("Arial", 12, "bold"),bg="#4CAF50", fg="white", width=20, command=run_algorithm).pack(pady=20)

tk.Button(root, text="Exit", font=("Arial", 11),bg="#f44336", fg="white", width=10, command=root.destroy).pack()

tk.Button(root, text="Show Stats", font=("Arial", 11), bg="#2196F3", fg="white", width=15, command=show_results).pack(pady=(0, 10))

root.mainloop()