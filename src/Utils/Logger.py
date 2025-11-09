
import pandas as pd


class Logger:
    def __init__(self):
        self.results = []

    def record(self, algo_name, best_distance, best_route, iterations):
        self.results.append({
            "Algorithm": algo_name,
            "Best Distance": best_distance,
            "Iterations": iterations,
            "Route": best_route
        })

    def save_csv(self, filepath):

        df_new = pd.DataFrame(self.results)


        try:
            df_existing = pd.read_csv(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df_combined = df_new


        df_combined.to_csv(filepath, index=False)

        self.results = []
        print(f"Results saved to {filepath}")

    def show_summary(self, filepath):
        pd.set_option('display.max_colwidth', None)
        df = pd.read_csv(filepath)
        print("Summary of Results:")
        print(df.sort_values("Best Distance").head(10)) 
