import tkinter as tk
from tkinter import ttk, messagebox
from src.TspSolver import TspSolver
from src.Ville import Ville
from src.Algorithms.randomSearch import randomSearch
from src.Algorithms.localSearch import localSearch



path = "data/algeria_20_cities_xy.csv"


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

    
    if algo == "Random Search":
        best_route, best_distance = randomSearch(villes, limit)
    elif algo == "Local Search":
        best_route, best_distance = localSearch(villes, limit)
    else:
        messagebox.showinfo("Info", "Selected algorithm not available yet.")
        return
    route_names = " → ".join([villes[i].name for i in best_route])
    messagebox.showinfo("Result", f"{algo} Finished!\n\n"f"Best Distance: {best_distance:.2f} km\n\n"f"Best Route:\n{route_names}"
    )



root = tk.Tk()
root.title("TSP Solver")
root.geometry("450x320")
root.resizable(False, False)


tk.Label(root, text="TSP Solver", font=("Arial", 18, "bold")).pack(pady=10)


tk.Label(root, text="Choose an algorithm:", font=("Arial", 12)).pack(pady=(10, 5))
algo_choice = ttk.Combobox(root, values=["Random Search", "Local Search", "Simulated Annealing"],state="readonly", font=("Arial", 12))
algo_choice.current(0)
algo_choice.pack(pady=5)


tk.Label(root, text="Number of iterations:", font=("Arial", 12)).pack(pady=(10, 5))
iter_entry = tk.Entry(root, font=("Arial", 12), justify="center")
iter_entry.insert(0, "1000")
iter_entry.pack(pady=5)

tk.Button(root, text="Run Algorithm", font=("Arial", 12, "bold"),bg="#4CAF50", fg="white", width=20, command=run_algorithm).pack(pady=20)

tk.Button(root, text="Exit", font=("Arial", 11),bg="#f44336", fg="white", width=10, command=root.destroy).pack()

root.mainloop()