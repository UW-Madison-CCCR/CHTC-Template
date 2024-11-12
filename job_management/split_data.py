import pandas as pd
import os

#================================================================
#
# split_data.py: divides the weather.csv dataset into multiple smaller datasets
#
#================================================================

# Reads in the data chunk-by-chunk (this approach scales well for large datasets)

# sets the number of rows to put in each chunk
chunksize = 500 # typically this number would be *much* larger; it's only this small for demo purposes

# specifies the file to read in
filepath = os.path.join('..', 'weather.csv')

# sets the output folder where each chunk will be saved
output_folder = os.path.join('..', 'split_data')

count = 0 # sets up an iterator to name the files
for chunk in pd.read_csv(filepath, chunksize=chunksize):

    # saves the new chunk as a dataframe to the output folder
    output_filename = os.path.join(output_folder, f'split_weather_{count}.csv')
    chunk.to_csv(output_filename)

    count += 1 # increases the count iterator