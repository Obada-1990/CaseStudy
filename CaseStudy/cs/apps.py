from django.apps import AppConfig
from externalScript import read_text_files

#directory = './testFiles'
directory = './archive/Stocks'

class CsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cs'
    def ready(self):
        read_text_files(directory)
        print("Server is ready and data is loaded")


 