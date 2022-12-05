
#Python code from question 2
import socket
print(socket.gethostname())

#Python code from question 4
my_list = [1, 2, 3]
print(f'My list is: {my_list}')




#Python code from question 6
"""
Source for matplotlib plotting: https://matplotlib.org/stable/tutorials/introductory/pyplot.html
Source for matplotlib arguments: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_ylim.html#matplotlib.axes.Axes.set_ylim
Source for pandas data handling: https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
Source for python counter: https://realpython.com/python-counter/
"""


#####Importing libraries####
import pandas as pd
import matplotlib.pyplot as plt
import math
import sklearn as sk
import numpy as np
import csv
############################

#####Defining method for reading and cleaning dataframes with pandas#####
def clean_df(file, thresh, samps): #thresh refers to theshold of dataframe length, file is either the file path or name of csv file, samps is the amount of samples to sample if DF length is > thresh
    df = pd.read_csv(file)
    df = df.dropna(axis = 1) #drops columns with nan values
    if len(df) > thresh:
        df = df.sample(n = samps, replace = False, random_state = 99) #if the length of DF is > thresh, the DF is samples without replacement for a smaller dataset to prevent system fault
    return df
#########################################################################
file = "/anvil/projects/tdm/data/flights/subset/1991.csv"
thresh = 5000
samples = 20000

Flight_data = clean_df(file, thresh, samples) #return clean data set


#####For a given month (integer) this function will take a list of months and CRSElapsed times, and find elapsed times >= time threshold (ELT) for given month#####
def month_arrivals(Months, CRSelts, Month_number, ELT): # months = list of months (integers), list of CRSelapsedTimes, Month_number = month as integer, ELT = threshold elapsed time
    month = 0
    ranges = list(range(len(CRSelts)))
    for i in ranges:
        if Months[i] == Month_number and CRSelts[i] >= ELT:
            month += 1
    return month
###################################################################################################################################################################
time_thresh = 200
elapsed_times = list(Flight_data["CRSElapsedTime"])
month_list = list(Flight_data["Month"])

counts = [] #empty list for adding times > time_thresh
month = list(range(1,13)) #list of months from 1-12

#####For loop to quick iterate through months 1-12 (Jan-Dec) without the need for making separate variables#####
for i in month:
    counts.append(month_arrivals(month_list, elapsed_times, i, time_thresh))
################################################################################################################


#list of month names to be used for the x-axis of a bar graph
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 

###Visualizing data
plt.bar(month_names, counts, align = 'center')
plt.ylim(150, 200)
plt.title('Counts of CRSElapsedTimes > 200')
plt.ylabel('Counts')
plt.xlabel('Month')
