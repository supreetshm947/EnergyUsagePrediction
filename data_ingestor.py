import pandas as pd
import glob

def prepare_data():
    energy_data  = pd.read_csv("data/power_consumption.csv", parse_dates={'datetime': ['Date', 'Time']},
                              infer_datetime_format=True, low_memory=True)

    energy_data["Global_active_power"] = pd.to_numeric(energy_data["Global_active_power"], errors='coerce')

    energy_data.set_index("datetime", inplace=True)

    energy_data_hourly = energy_data["Global_active_power"].resample("H").mean()


    weather_files = glob.glob("data/PARIS_MONTSOURIS_*.csv")

    weather_data = pd.concat([pd.read_csv(file, parse_dates=["DATE"], low_memory=True) for file in weather_files])

    weather_data = weather_data.loc[:, ["DATE", "TMP", "DEW", "SLP","WND", "VIS"]]
    weather_data.set_index("DATE", inplace=True)

