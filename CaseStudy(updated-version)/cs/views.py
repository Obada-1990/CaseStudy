from django.shortcuts import render,redirect
from django.http import HttpResponse
from externalScript import getMaxMinDates, plotDataA, plotDataB, getNonInvestmentQuote, get_hm

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
         with open("plot_1.png", "rb") as img:
            image = img.read()
    return HttpResponse(image, content_type="image/png")  

def getNonInvQuote(request):
     if request.method == 'GET':
          NonInvQuote = getNonInvestmentQuote()   
     return render(request, 'website.html', {'data_NIQ': NonInvQuote}) 

def plot_dataB_or_hm(request):
    if request.method == 'POST':
       fondsVolumenStr = request.POST.get('fond_volumen')
       titelZahlStr = request.POST.get('titel_zahl')
       fondsVolumenInt = int(fondsVolumenStr) # convert to Int
       titelZahlInt = int(titelZahlStr) # convert to Int
       if 'plot_B' in request.POST:
         plotDataB(fondsVolumenInt,titelZahlInt)
         with open("plot_2.png", "rb") as img:
                image = img.read()
       elif 'hm' in request.POST:
           get_hm(fondsVolumenInt,titelZahlInt)
           with open("plot_3.png", "rb") as img: # file is closed after reading
             image = img.read()
  
    return HttpResponse(image, content_type="image/png") 
    



def delete(request):
    if request.method == 'POST':
      data_delete = None
    elif 'clean_delete' in request.POST: # to clear the board
       data_delete = None
    return render(request, 'website.html', {'data_do': data_delete}) 

