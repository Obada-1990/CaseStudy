from django.urls import path
from . import views

#URLConfig
urlpatterns = [
    path('casestudy/', views.home_view),
    path('delete/', views.delete, name = 'delete'),
    path('dates/', views.get_dates, name = 'get_dates'),
    path('niq/', views.getNonInvQuote, name = 'getNonInvQuote'),
    path('plota/', views.plot_dataA, name = 'plot_dataA'),
    path('plotb/', views.plot_dataB, name = 'plot_dataB'),

    ]
