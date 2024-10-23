import pandas as pd
import sys

#================================================================
#
# Step 1: Set Up the Function
#
#================================================================

# convert_data: converts the temperature data to celsius and calculates the wind chill
# returns a converted dataframe
'''
Arguments:
* data_path: a string for the filepath to the csv file containing the data to convert
'''
def convert_data(data_path: str):

    # reads in the data from the filepath
    df = pd.read_csv(data_path)

    # gets the average celsius temp between the min and max
    df['temp_avg'] = (df['temp_max'] + df['temp_min']) / 2

    # converts the average temperature to celsius
    df['temp_f'] = df['temp_avg'] * 9/5 + 32

    # calculate_wind_chill: nested function for converting wind chill data
    # returns a float representing the wind chill in Fahrenheit
    '''
    Arguments:
    * temp_f: temperature in Fahrenheit
    * wind: wind speed
    '''
    def calculate_wind_chill(temp_f: float, wind: float):
        return 35.74 + 0.6215 * temp_f  - 35.75 * (wind ** 0.16) + 0.4275 * temp_f * (wind ** 0.16)

    # calculates the wind chill
    df['wind_chill'] = df.apply(lambda x:  calculate_wind_chill(x['temp_f'], x['wind']), axis=1)

    return df

#================================================================
#
# Step 2: Call the Function, Passing a System Argument
#
#================================================================

# calls the convert_data function on the specified filepath
# uses the first system argument passed from the shell script
convert_data(sys.argv[1])