from asyncio.log import logger
import tkinter as tk
from tkinter import ttk, messagebox
from src.TspSolver import TspSolver
from src.Algorithms.randomSearch import randomSearch
from src.Algorithms.localSearch import localSearch
from src.Algorithms.hillClimbing import hillClimbing
from src.Algorithms.simulatedAnnealing import simulatedAnnealing
from src.Algorithms.tabuSearch import tabuSearch

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
            best_route, best_distance = localSearch(villes, distance_matrix, limit, radius=2, visual=visual)
    elif algo == "Recherche Hill climbing":
        best_route, best_distance = hillClimbing(villes, distance_matrix, limit, visual=visual)
    elif algo == "Recherche Recuit-Simulé":
        try:
            temperature = float(temp_entry.get())
            cooling_rate = float(cooling_entry.get())
            if temperature <= 0:
                raise ValueError("Temperature must be > 0")
            if not (0 < cooling_rate < 1):
                raise ValueError("Cooling rate must be between 0 and 1 (exclusive)")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid simulated annealing parameters: {e}")
            return
            
        best_route, best_distance = simulatedAnnealing(villes, distance_matrix, temperature, cooling_rate, limit, visual=visual)

    elif algo == "Recherche Tabu":
        tabu_size = 15
        neighborhood_size = 100
        best_route, best_distance = tabuSearch(villes, distance_matrix, limit, tabu_size, neighborhood_size, visual=visual)
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


tk.Label(root, text="Number of iterations:", font=("Arial", 12)).pack(pady=(10, 5))
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

def show_or_hide_sa_fields(event=None):
    if algo_choice.get() == "Recherche Recuit-Simulé":
        temp_label.pack(pady=(8, 2))
        temp_entry.pack(pady=2)
        cooling_label.pack(pady=(8, 2))
        cooling_entry.pack(pady=2)
    else:
        temp_label.pack_forget()
        temp_entry.pack_forget()
        cooling_label.pack_forget()
        cooling_entry.pack_forget()

algo_choice.bind("<<ComboboxSelected>>", show_or_hide_sa_fields)

show_or_hide_sa_fields()

tk.Button(root, text="Run Algorithm", font=("Arial", 12, "bold"),bg="#4CAF50", fg="white", width=20, command=run_algorithm).pack(pady=20)

tk.Button(root, text="Exit", font=("Arial", 11),bg="#f44336", fg="white", width=10, command=root.destroy).pack()

tk.Button(root, text="Show Results", font=("Arial", 11), bg="#2196F3", fg="white", width=15, command=show_results).pack(pady=(0, 10))

root.mainloop()