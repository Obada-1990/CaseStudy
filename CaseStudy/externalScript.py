import os # accessing directory structure
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import timeit
import pandas as pd
from collections import defaultdict


dataArr = []

#directory = './testFiles'
directory = './archive/Stocks'
def read_text_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            if os.path.getsize(path) > 0: # escape empty files
                with open(path, "r") as file:
                    lines = file.readlines()
                    for line in lines[1:]:  
                        content = line.strip().split(',')
                        dateStr = datetime.strptime(str(content[0]), "%Y-%m-%d").date() 
                        volume = content[5]
                        newContent = filename, dateStr, volume
                        dataArr.append(newContent)
            else:
                pass            
 
#**************************************************************#
                          # 1.a 
    # #Answer = MinDate: 1962-01-02  MaxDate: 2017-11-10
#**************************************************************#
def getMaxMinDates(): #read the data into dic
    dates =  [x[1] for x in dataArr]
    maxDate = max(dates)
    minDate = min(dates)
    return minDate, maxDate

#**************************************************************#
                         # 1.b 
 # sum all volumes for the same date and calculate the average
#**************************************************************#
def prepareData(): 
    data = {}  
    dates =  [x[1] for x in dataArr]
    volumes =  [x[2] for x in dataArr]
    i = 0
    while i < len(dates):
        if dates[i] in data:
            data[dates[i]].append(float(volumes[i]))
        else:   # If the date is not in the dictionary, create a new entry
            data[dates[i]] = [float(volumes[i])]  
        i += 1        
    return data        
 
def getAverage(data):
    avgData = {}
    i = 0
    keys = list(data.keys())
    while i < len(keys):
        key = keys[i]
        value = data[key]
        avgData[key] = sum(value) / len(value) 
        i += 1
    return avgData
 

def plotDataA():
    data = prepareData()
    average = getAverage(data) # dic for each date and its average e.g {'2005-02-01': 66.66, '2005-02-02': 125.0, '2005-02-03': 60.0}
    sortedList = sorted(average.items(), reverse=False) #order by date asc -> return a list
    dates = [d[0] for d in sortedList]
    values = [d[1] for d in sortedList]
    data2 = pd.DataFrame({'date': dates, 'value': values})
    data2['date'] = pd.to_datetime(data2['date'])
    data2.set_index('date', inplace=True)
    downsampled = data2.resample('W').mean()
    plt.plot(downsampled.index, downsampled['value'], color='red', linestyle='-', linewidth=2)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Downsampled Data Over Time')
    plt.savefig("plot_1.png")
    plt.show()
    plt.close()
     
#**************************************************************#
                         # 2.a
 # sum all volumes for the same date and calculate the average
#**************************************************************#

def getPlotData(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    # Create an empty dictionary to store the dataframes
    dataframes = {}
    dayNr = 80
    # Loop through all the text files
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.getsize(file_path) > 0: # escape empty files
            df = pd.read_csv(file_path)
            df.sort_values(by='Date', ascending=True, inplace=True)
            max_date = df['Date'].max()
            start_date = pd.to_datetime(max_date) - pd.Timedelta(days=dayNr)
            dateStr = df['Date']
            date = pd.to_datetime(dateStr) 
            last_60_days = df[date >= start_date]  
            workingDays = pd.bdate_range(start=start_date, end=max_date)
            while len(workingDays) != 60:
                dayNr = dayNr + 1
                start_date = pd.to_datetime(max_date) - pd.Timedelta(days=dayNr)
                workingDays = pd.bdate_range(start=start_date, end=max_date)
            avg = last_60_days['Volume'].mean()    
            dataframes[file] = avg
        else:
            pass    
    return dataframes


NonInvestmentQuote = []

def plotDataB(fondsVolumen: int, titelZahl: int):
    dataDic = getPlotData(directory)
    threshold = fondsVolumen/titelZahl
    xData = []
    yData = []
    overAllData = {}
    sortedList = []
    for title, values in dataDic.items():
         overAllData[title] = values
         sortedList = sorted(overAllData.items(), key=lambda values: values[1]) #sort values asc
         xData = [x[0] for x in sortedList]# assign titles
         yData = [x[1] for x in sortedList]# assign values
    x = np.array(xData)
    y = np.array(yData)
    belowThreshold = y < threshold  # Identify all points below the threshold e.g [True True False]
    trueCount = np.sum(belowThreshold)  # averages below threshold
    percentage = (trueCount / len(belowThreshold)) 
    NonInvestmentQuote.append(percentage)
    plt.plot(x, y, label="Data")
    plt.scatter(x[belowThreshold], y[belowThreshold], color="red", label="Below Threshold") # Plot the points below the threshold
    plt.axhline(threshold, color="green", linestyle="--", label="Threshold")  # Add a horizontal line to represent the threshold
    plt.legend()
    plt.xlabel("Titel")  # Titel (in aufsteigender Reihenfolge je nach durchschnittlichem täglichen Handelsvolumen)
    plt.ylabel("durchschnittliches tägliches Handelsvolumen (60 Tage)")
    plt.savefig("plot_2.png")
    plt.show()
    plt.close()


def getNonInvestmentQuote():
    if len(NonInvestmentQuote) > 0:
        percentageNIQ = "{:.2%}".format(NonInvestmentQuote[0]) #e.g 2/3 -> 66.67%
    else:
        percentageNIQ = "0.00%"  
    return percentageNIQ

#**************************************************************#
                        #2.b
                      #Heatmap
#**************************************************************#

