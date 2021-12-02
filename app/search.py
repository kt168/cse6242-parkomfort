import pandas as pd

def load_meters(path:str) -> pd.DataFrame:
    meters = pd.read_csv(path)
        

    return meters