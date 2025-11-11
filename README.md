# TSP Solver

A Python-based Traveling Salesman Problem (TSP) solver with a graphical user interface. This project implements multiple optimization algorithms to find the shortest route visiting all cities exactly once.

## Features

- **Multiple Algorithms**: Implements various optimization algorithms including:
  - Random Search
  - Local Search
  - Hill Climbing
  - Simulated Annealing
  - Tabu Search
  - Genetic Algorithm

- **Graphical User Interface**: User-friendly Tkinter-based GUI for easy algorithm selection and visualization of results

- **Real-world Data**: Uses Algerian cities dataset with actual coordinates

- **Flexible Configuration**: Adjustable iteration limits for optimization algorithms

## Requirements

- Python 3.x
- pandas
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DMKeyy/TspSolver.git
cd TSP_Problem
```

2. Install required dependencies:
```bash
pip install pandas matplotlib
```

## Usage

Run the application:
```bash
python main.py
```

The GUI will open, allowing you to:
1. Select an optimization algorithm from the dropdown menu
2. Set the number of iterations
3. Click "Run Algorithm" to execute
4. View the best route and distance in the results dialog


## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is available for educational and research purposes.


