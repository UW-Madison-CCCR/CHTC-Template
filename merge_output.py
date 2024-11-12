import pandas as pd
import os

#================================================================
#
# Iterates through the output files and merges them
#
#================================================================

# gets a list of output weather files in the base directory
files = [f for f in os.listdir('.') if 'output_weather_' in f]

# creates a template for the output
output = pd.DataFrame()

# combines them through concatenation (if small enough to fit in memory)
for file in files:

    # reads in the file
    df = pd.read_csv(file)

    # adds it to the output template
    output = pd.concat([output, df])

# saves the file
output.to_csv('weather_converted.csv')