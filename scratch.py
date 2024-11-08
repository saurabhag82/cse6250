import pandas as pd

# Load the CSV file
csv_file = 'data/x.csv'      # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Save as HDF5
h5_file = 'data/X.h5'        # Replace with your desired HDF5 file path
df.to_hdf(h5_file, key='X', mode='w')