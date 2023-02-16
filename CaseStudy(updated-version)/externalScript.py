import os 
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

#**************************************#
            #load data
#**************************************#
#directory = './testFiles' 
directory = './archive/Stocks'
pureData = {}
def prepare_data(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.getsize(file_path) > 0: # escape empty files
            df = pd.read_csv(file_path)
            df.drop(columns=["Open", "High", "Low", "Close", "OpenInt"],inplace=True,axis =1) # drop unnecessary columns
            df.sort_values(by='Date', ascending=True, inplace=True)
            pureData[file] = df
        else:
            pass    
           
#**************************************************************#
                          # 1.a 
    # #Answer = MinDate: 1962-01-02  MaxDate: 2017-11-10
#**************************************************************#
def getMaxMinDates():
    dates = [datetime.strptime(date_str, '%Y-%m-%d').date() for value in pureData.values()
         for date_str in value['Date']]
    max_date = max(dates)
    min_date = min(dates)
    return min_date, max_date

#**************************************************************#
                         # 1.b 
 # sum all volumes for the same date and calculate the average
#**************************************************************#
def plotDataA():
    data = {} # each date with all volumes fpor the same date e.g. '2005-02-01': [100, 60, 40]
    averages = {}
    for value in pureData.values():
        dates = value['Date']
        volumes = value['Volume']
        for date, volume in zip(dates, volumes):
            if date not in data:
                data[date] = []
            data[date].append(volume)

    for date, volume in data.items(): # calculate average for each date e.g. {'2005-02-01': 67}
        averages[date] = round(sum(volume) / len(volume))

    sorted_averages = sorted(averages.items(), reverse=False) #order by date asc -> return a list
    df = pd.DataFrame({'Date':[x[0] for x in sorted_averages] , 'Average':[x[1] for x in sorted_averages]}) # convert to dataframe
    df.set_index(pd.to_datetime(df['Date']), inplace=True) # convert date to datetime and set it as index
    #--------------------------downsampled weekly-----------------------------#
    #downsampled = df.resample('W').mean(numeric_only=True).fillna(0)  #downsample the data
    #plt.plot(downsampled.index, downsampled.values, color='red', linestyle='-', linewidth=2)
    #plt.subplots(figsize=(50, 25)) 
    fig, ax = plt.subplots(figsize=(30, 25)) 
    df.plot(ax=ax)
    ax.set_xticks(df.index, rotaion=90)
    plt.xlabel('Zeit')
    plt.ylabel('Durchschnitt tägliches Handelsvolumen')
    plt.title('Tägliche Handelsvolumen über die gesamte Zeitspanne')
    plt.savefig("plot_1.png")
    #plt.show()
    plt.close()
     
#**************************************************************#
                         # 2.a
 # sum all volumes for the same date and calculate the average
#**************************************************************#
def getPlotData():
    plotData = {}
    dayNr = 80
    for key, values in pureData.items():
        maxDate = values['Date'].max()
        startDate = pd.to_datetime(maxDate) - pd.Timedelta(days=dayNr)
        dateStr = values['Date']
        date = pd.to_datetime(dateStr) 
        lastSixtyDaysData = values[date >= startDate]  
        workingDays = pd.bdate_range(start=startDate, end=maxDate)
        while len(workingDays) != 60:
           dayNr = dayNr + 1
           startDate = pd.to_datetime(maxDate) - pd.Timedelta(days=dayNr)
           lastSixtyDaysData = values[date >= startDate]  
           workingDays = pd.bdate_range(start=startDate, end=maxDate)
        df = pd.DataFrame(lastSixtyDaysData)   
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        #-----------------downsampled--------------------#
        #downSampled = df.resample('W').mean() 
        #avg = downSampled['Volume'].mean()  
        avg = df['Volume'].mean()  
        plotData[key] = avg
    return plotData


NonInvestmentQuote = []
def plotDataB(fondsVolumen: int, titelZahl: int):
    dataDic = getPlotData()
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

    np.set_printoptions(suppress=True) #suppress scientific notation
    x = np.array(xData) # titels
    y = np.array(yData) # averages round(2 numbers after comma)
    y_rounded = np.round(y, decimals=2)
    belowThreshold:int = y_rounded < threshold  # Identify all points below the threshold e.g [True True False]
    trueCount = np.sum(belowThreshold)  # averages below threshold
    percentage = (trueCount / len(belowThreshold)) 
    NonInvestmentQuote.append(percentage)
    plt.subplots(figsize=(30, 20))
    plt.plot(x, y_rounded, label="Data")
    plt.xticks(rotation = 90) #x labels rotation
    plt.scatter(x[belowThreshold], y_rounded[belowThreshold], color="red", label="Below Threshold") # Plot the points below the threshold
    plt.axhline(threshold, color="green", linestyle="--", label="Threshold")  # Add a horizontal line to represent the threshold
    plt.legend()
    plt.title('Durchschnittliche tägliche Handelsvolumen pro Aktie über die letzten 60 Handelstage in aufsteigender Reihenfolge')
    plt.xlabel("Titel")  # Titel (in aufsteigender Reihenfolge je nach durchschnittlichem täglichen Handelsvolumen)
    plt.ylabel("durchschnittliches tägliches Handelsvolumen (60 Tage)")
    plt.savefig("plot_2.png")
    #plt.show()
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
def get_hm(fondsVolumen: int, titelZahl: int):
    plot_data = getPlotData()
    averages =[round(x) for x in plot_data.values()] # get averages fro dic and round them 
    sortedAverages = sorted(averages, reverse=False) #sort the list of averages
    threshold = fondsVolumen / titelZahl
    list_len = len(sortedAverages)
    num_rows = int(np.sqrt(list_len))
    rest= list_len%num_rows
    while rest > 0:
         sortedAverages += [0]
         list_len = len(sortedAverages)
         num_rows = int(np.sqrt(list_len))
         rest= list_len%num_rows
    num_cols = int(np.ceil(list_len/num_rows))     
    averages_array = np.array(sortedAverages).reshape(num_rows, num_cols) # rehshape the array.In this case(84, 86)
    fig, hm = plt.subplots(figsize=(30, 20)) 
    hm=sns.heatmap(averages_array, cmap="Reds", vmin=threshold,  annot=True, fmt=".0f", cbar=False, xticklabels=1, yticklabels=1)
    hm=sns.heatmap(averages_array, cmap="RdBu", vmax=threshold, center=0, annot=True, fmt=".0f", cbar=False,  xticklabels=1, yticklabels=1)
    x_labels = np.arange(200000000, 5000000000, 10) # Fondsvolumen
    y_labels = np.arange(50, 4000, 10) # Titelzahl
    #x_labels_mapped = [f"{num/1000000000:.0f} Mrd" if num % 1000000000 == 0 else f"{num} Mio" for num in x_labels]
    hm.set_xticklabels(x_labels[:averages_array.shape[1]], rotation=45)   #86 
    hm.set_yticklabels(y_labels[:averages_array.shape[0]]) #84
    plt.savefig("plot_3.png")
    #plt.show()
    plt.close()
    

#**************************************************************#
            #Heatmap for values belwo threshold
#**************************************************************#
def get_hm_below_th(fondsVolumen: int, titelZahl: int):
        plot_data = getPlotData()
        averages =[round(x) for x in plot_data.values()] # get averages fro dic and round them 
        sortedAverages = sorted(averages, reverse=False) #sort the list of averages
        threshold = fondsVolumen / titelZahl
        averages_below_threshold =[avergae for avergae in sortedAverages if avergae <= threshold] #get averagegs below threshold
        list_len = len(averages_below_threshold)
        num_rows = int(np.sqrt(list_len))
        rest= list_len%num_rows
        while rest > 0:
            averages_below_threshold += [0]
            list_len = len(averages_below_threshold)
            num_rows = int(np.sqrt(list_len))
            rest= list_len%num_rows
        num_cols = int(np.ceil(list_len/num_rows))     
        averages_below_th_array = np.array(averages_below_threshold).reshape(num_rows, num_cols) # rehshape the array.In this case(84, 86)
        max_value = np.max(averages_below_th_array) #minvalue must be less than or equal to maxvalue in the array
        fig, hm = plt.subplots(figsize=(30, 20)) 
        hm=sns.heatmap(averages_below_th_array, cmap="Reds", vmin=max_value,  annot=False, fmt=".0f", cbar=False)
        hm=sns.heatmap(averages_below_th_array, cmap="RdBu", vmax=threshold, center=0, annot=False, fmt=".0f", cbar=False)
        plt.savefig("plot_4.png")
        #plt.show()
        plt.close()


#prepare_data(directory)
#get_hm(2000000000,200)