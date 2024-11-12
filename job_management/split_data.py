import pandas as pd
import os

#================================================================
#
# Step 1: Divides weather.csv into multiple smaller datasets
#
#================================================================

# Reads in the data chunk-by-chunk (this approach scales well for large datasets)

# sets the number of rows to put in each chunk
chunksize = 500 # typically this number would be *much* larger; it's only this small for demo purposes

# specifies the file to read in
filepath = os.path.join('..', 'weather.csv')

# sets the output folder where each chunk will be saved
output_folder = os.path.join('..', 'split_data')

count = 0 # sets up an iteration counter to name the files
for chunk in pd.read_csv(filepath, chunksize=chunksize):

    # saves the new chunk as a dataframe to the output folder
    output_filename = os.path.join(output_folder, f'weather_{count}.csv')
    chunk.to_csv(output_filename)

    count += 1 # increases the count

#================================================================
#
# Step 2: Saves those datasets into a list for later iteration
#
#================================================================

# gets the list of files from the output folder
# sticks to csv files to avoid opening a .DS_Store file
files = [f for f in os.listdir(output_folder) if '.csv' in f]

# converts the file list to a string separated by a new line
file_text = '\n'.join(files)

# saves this text to a file list .txt file
file_list_path = os.path.join(output_folder, 'file_list.txt')
with open(file_list_path, 'w') as f:
    f.write(file_text)