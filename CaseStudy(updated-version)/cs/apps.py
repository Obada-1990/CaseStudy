from django.apps import AppConfig
from externalScript import prepare_data
from termcolor import colored

#directory = './testFiles' 
directory = './archive/Stocks'

class CsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cs'
    def ready(self):
        prepare_data(directory)
        print(colored("Server is up and data has been loaded", "red", attrs=["bold"]))


 