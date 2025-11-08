import matplotlib.pyplot as plt

def visualize_route(villes, route, title):

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