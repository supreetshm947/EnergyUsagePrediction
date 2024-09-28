import pandas as pd
import glob
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import mutual_info_regression
from sklearn.impute import SimpleImputer
import numpy as np


def fetch_data_as_df():
    energy_data = pd.read_csv("data/power_consumption.csv", parse_dates={'datetime': ['Date', 'Time']},
                              infer_datetime_format=True, low_memory=True)
    energy_data["Global_active_power"] = pd.to_numeric(energy_data["Global_active_power"], errors='coerce')
    energy_data.set_index("datetime", inplace=True)
    energy_data_hourly = energy_data["Global_active_power"].resample("H").mean().to_frame()

    energy_data_hourly['Hour'] = energy_data_hourly.index.hour
    energy_data_hourly['DayOfWeek'] = energy_data_hourly.index.dayofweek
    energy_data_hourly['Month'] = energy_data_hourly.index.month
    energy_data_hourly['Year'] = energy_data_hourly.index.year

    # Parsing Weather data
    weather_files = glob.glob("data/PARIS_MONTSOURIS_*.csv")
    weather_data = pd.concat([pd.read_csv(file, parse_dates=["DATE"], low_memory=True) for file in weather_files])
    weather_data = weather_data.loc[:, ["DATE", "TMP", "DEW", "SLP", "WND", "VIS"]]

    invalid_values = {
        "TMP": 9999,
        "DEW": 9999,
        "SLP": 99999,
        "VIS": 999999,
        "Wind_Direction": 999,
        "Wind_Speed": 0
    }

    for col in ["TMP", "DEW", "SLP", "VIS"]:
        weather_data[col] = pd.to_numeric(weather_data[col].str.split(",", expand=True)[0], errors="coerce")
        weather_data[col] = weather_data[col].replace(invalid_values[col], np.nan) / 10

    # WND needs special parsing
    # weather_data[["Wind_Direction", "_", "_", "Wind_Speed", "_"]] = (
    #     weather_data["WND"].str.split(",", expand=True))

    weather_data['Wind_Direction'] = (pd.to_numeric(weather_data["WND"].str.split(",", expand=True)[0], errors='coerce')).replace(
        invalid_values['Wind_Direction'], np.nan)
    weather_data['Wind_Speed'] = (pd.to_numeric(weather_data["WND"].str.split(",", expand=True)[3], errors='coerce')).replace(
        invalid_values['Wind_Speed'], np.nan)/ 10

    # Drop the original WND column after extracting components
    weather_data.drop(columns=['WND'], inplace=True)

    weather_data.set_index("DATE", inplace=True)

    combined_data = pd.merge(left=energy_data_hourly, right=weather_data, left_index=True, right_index=True,
                             how="inner")

    my_imputer = SimpleImputer()
    combined_data_imputed = pd.DataFrame(my_imputer.fit_transform(combined_data),
                                         columns=combined_data.columns,
                                         index=combined_data.index)

    combined_data_imputed["data_aggr"] = combined_data_imputed['Hour'] + combined_data_imputed['DayOfWeek'] + combined_data_imputed['Month']
    return combined_data_imputed

def get_mutual_info(data):
    y = data.pop("Global_active_power")
    X = data
    mi_scores = mutual_info_regression(X, y)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    print(mi_scores)

def scale_features(data):
    data_np = data.values

    features = data_np[:, 1:]
    target = data_np[:, 0]

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)


def get_data():
    df = fetch_data_as_df()
    get_mutual_info(df)


get_data()
