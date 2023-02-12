from django.shortcuts import render,redirect
from django.http import HttpResponse
from externalScript import getMaxMinDates, plotDataA, plotDataB, getNonInvestmentQuote

def home_view(request):
        return render(request, 'website.html')
    
def get_dates(request):
    if request.method == 'POST':
        dates = getMaxMinDates()
        data_dates = f"MaxDate = {dates[1]}    MinDate = {dates[0]}"
    return render(request, 'website.html', {'data_dates': data_dates})  # render the data
    
def plot_dataA(request):
    if request.method == 'GET':
         plotDataA()
         with open("plot_1.png", "rb") as f:
            image_data_A = f.read()
    return HttpResponse(image_data_A, content_type="image/png")  

def getNonInvQuote(request):
     if request.method == 'GET':
          NonInvQuote = getNonInvestmentQuote()   
     return render(request, 'website.html', {'data_NIQ': NonInvQuote}) 

def plot_dataB(request):
    if request.method == 'POST':
       fondsVolumenStr = request.POST.get('fond_volumen')
       titelZahlStr = request.POST.get('titel_zahl')
       fondsVolumenInt = int(fondsVolumenStr)
       titelZahlInt = int(titelZahlStr)
       plotDataB(fondsVolumenInt,titelZahlInt)
       with open("plot_2.png", "rb") as f:
            image_data_B = f.read()
    return HttpResponse(image_data_B, content_type="image/png") 

def delete(request):
    if request.method == 'POST':
      data_delete = None
    elif 'clean_delete' in request.POST: # to clear the board
       data_delete = None
    return render(request, 'website.html', {'data_do': data_delete}) 

