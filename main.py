from ucimlrepo import fetch_ucirepo
import os

def fetch_data(path:str = "./data"):
    os.makedirs(path, exist_ok=True)

    individual_household_electric_power_consumption = fetch_ucirepo(id=235)
    X = individual_household_electric_power_consumption.data.features
    X.to_csv(X.to_csv(f"{path}/power_consumption.csv", index=False), index=False)

if __name__ == "__main__":
    fetch_data()