
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

    def get_summary(self, filepath):
        pd.set_option('display.max_colwidth', None)
        df = pd.read_csv(filepath)
        print("Summary of Results:")
        return df.sort_values("Best Distance").drop_duplicates(subset=['Best Distance']).drop_duplicates(subset=['Route']).head(10) 


    def show_best_per_algorithm(self, filepath):
        pd.set_option('display.max_colwidth', None)
        df = pd.read_csv(filepath)

        df['Best Distance'] = pd.to_numeric(df['Best Distance'], errors='coerce')

        best_min = df.groupby('Algorithm', as_index=False)['Best Distance'].min()

        best_rows = pd.merge(best_min, df, on=['Algorithm', 'Best Distance'], how='left').drop_duplicates(subset=['Algorithm'])

        best_rows = best_rows.sort_values('Best Distance').reset_index(drop=True)

        print("Best distance per algorithm:")
        print(best_rows[['Algorithm', 'Best Distance', 'Route', 'Iterations']])

    def get_avg_per_algo(self, filepath):
        df = pd.read_csv(filepath)
        df['Best Distance'] = pd.to_numeric(df['Best Distance'], errors='coerce')
        return df.groupby('Algorithm')['Best Distance'].mean().sort_values()
    
    def get_best_per_algo(self, filepath):
        df = pd.read_csv(filepath)
        df['Best Distance'] = pd.to_numeric(df['Best Distance'], errors='coerce')
        return df.groupby('Algorithm')['Best Distance'].min().sort_values()