import pandas as pd

def generate_lstm_features(initial_icu_stay_period):
    labs_and_vitals_df = pd.read_csv('../data/labs_and_vitals.csv')



if __name__ == "__main__":
    generate_lstm_features(24)