from django.urls import path
from . import views

#URLConfig
urlpatterns = [

    path('casestudy/', views.home_view),
    path('delete/', views.delete, name = 'delete'),
    path('dates/', views.get_dates, name = 'get_dates'),
    path('niq/', views.getNonInvQuote, name = 'getNonInvQuote'),
    path('plota/', views.plot_dataA, name = 'plot_dataA'),
    path('plotb_hm/', views.plot_dataB_or_hm, name = 'plot_dataB_or_hm'),

    ]