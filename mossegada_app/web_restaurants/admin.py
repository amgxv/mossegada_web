from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from web_restaurants.models import Restaurant,TypeRestaurants,Ratings,Profile

# Importa els models a administrar.
# En aquest cas registram 4 models amb opció d'emprar Import/Export per poder gestionar les dades mitjançant un csv o derivats.
# Cridam a la funció admin.site.register i li passam els arguments (Model, ImportExportModelAdmin)

admin.site.register(Restaurant,ImportExportModelAdmin)
admin.site.register(TypeRestaurants,ImportExportModelAdmin)
admin.site.register(Ratings,ImportExportModelAdmin)
admin.site.register(Profile, ImportExportModelAdmin)


