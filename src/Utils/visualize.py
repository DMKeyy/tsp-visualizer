import matplotlib.pyplot as plt

    
def visualize_route(villes, route, title):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    x = [villes[i].x for i in route]
    y = [villes[i].y for i in route]

    plt.plot(x, y, marker='o', color='orange', linewidth=2, markersize=8)

    for i in route:
        plt.text(villes[i].x + 5, villes[i].y + 5, villes[i].name, fontsize=9)

    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show(block=False)


def setup_live_plot(villes, figsize=(8, 6)):

    plt.ion()
    fig, ax = plt.subplots(figsize=figsize)

    x_cities = [v.x for v in villes]
    y_cities = [v.y for v in villes]

    ax.scatter(x_cities, y_cities, color='royalblue', s=60, zorder=3)
    for v in villes:
        ax.text(v.x + 10, v.y + 10, v.name, fontsize=8)

    current_line, = ax.plot([], [], color='skyblue', linewidth=1.5, label='Current Route')
    best_line, = ax.plot([], [], color='orange', linewidth=2.5, label='Best Route')

    return plt, fig, ax, current_line, best_line


def update_live_plot(villes, current_line, best_line, route, best_route, ax, title=None):

    x = [villes[j].x for j in route]
    y = [villes[j].y for j in route]
    current_line.set_data(x, y)

    if best_route:
        x_best = [villes[j].x for j in best_route]
        y_best = [villes[j].y for j in best_route]
        best_line.set_data(x_best, y_best)

    if title is not None:
        ax.set_title(title)



    plt.pause(0.001)


def finalize_live_plot(plt):
    plt.ioff()
    plt.show(block=False)

def plot_average_distance(avg_series):
    plt.figure(figsize=(8,6))
    ax = avg_series.plot(kind='bar', color='royalblue', edgecolor='black')
    plt.title("Average Distance per Algorithm")
    plt.ylabel("Average Distance (km)")
    plt.xlabel("Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for p in ax.patches:
        height = p.get_height()
        try:
            label = f"{height:.2f} km"
        except Exception:
            label = str(height)
        ax.annotate(label,
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom',
                    fontsize=9, xytext=(0, 3), textcoords='offset points')

    plt.tight_layout()
    plt.show(block=False)

def plot_best_distance(best_series):
    plt.figure(figsize=(8,6))
    ax = best_series.plot(kind='bar', color='orange', edgecolor='black')
    plt.title("Best Distance per Algorithm")
    plt.ylabel("Distance (km)")
    plt.xlabel("Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for p in ax.patches:
        height = p.get_height()
        try:
            label = f"{height:.2f} km"
        except Exception:
            label = str(height)
        ax.annotate(label,
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom',
                    fontsize=9, xytext=(0, 3), textcoords='offset points')

    plt.tight_layout()
    plt.show(block=False)
