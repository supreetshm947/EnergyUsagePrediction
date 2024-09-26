import pandas as pd

# energy_data  = pd.read_csv("data/power_consumption.csv", parse_dates={'datetime': ['Date', 'Time']},
#                           infer_datetime_format=True, low_memory=True)
#
# energy_data["Global_active_power"] = pd.to_numeric(energy_data["Global_active_power"], errors='coerce')
#
# energy_data.set_index("datetime", inplace=True)
#
# energy_data_hourly = energy_data["Global_active_power"].resample("H").mean()



weather_data_2006 = pd.read_csv("data/PARIS_MONTSOURIS_2006.csv", parse_dates=['DATE'],
                           low_memory=True)
weather_data_2007 = pd.read_csv("data/PARIS_MONTSOURIS_2007.csv", parse_dates=['DATE'],
                           low_memory=True)
weather_data_2008 = pd.read_csv("data/PARIS_MONTSOURIS_2008.csv", parse_dates=['DATE'],
                           low_memory=True)
weather_data_2009 = pd.read_csv("data/PARIS_MONTSOURIS_2009.csv", parse_dates=['DATE'],
                           low_memory=True)
weather_data_2010 = pd.read_csv("data/PARIS_MONTSOURIS_2010.csv", parse_dates=['DATE'],
                           low_memory=True)

weather_data = [weather_data_2006, weather_data_2007, weather_data_2008, weather_data_2009, weather_data_2010]

weather_data = pd.concat(weather_data).loc["DATE", "SOURCE"]