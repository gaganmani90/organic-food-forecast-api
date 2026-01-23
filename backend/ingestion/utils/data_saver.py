import os
import pandas as pd

OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), 'output'))
os.makedirs(OUTPUT_DIR, exist_ok=True)

class DataSaver:
    @staticmethod
    def save_to_csv(data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"📂 Data saved: {filename}")

    @staticmethod
    def save_to_json(data, filename):
        df = pd.DataFrame(data)
        df.to_json(filename, orient="records")
        print(f"📂 Data saved: {filename}")
