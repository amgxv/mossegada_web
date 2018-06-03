"""RestaurantsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


## Definició d'URLs general del Projecte.

from django.contrib import admin
from django.urls import include, path

'''
Inclou tots els paths de les aplicacions "web_restaurants" i admin.
Aqui podriem tenir diferents aplicacions funcionant a la vegada amb una configuració específica del projecte general.
Per exemple : 
    - WEB_RESTAURANTS - aplicació : web_restaurants | ../
    - API REST - aplicació : api_rest | ../api_rest
    - WEB_RECURSOS_HUMANS - aplicació : recursos_humans | /rrhh
    - PANELL ADMINISTRACIó - aplicació : admin | /admin
'''

urlpatterns = [
    path('', include('web_restaurants.urls')),
    path('admin/', admin.site.urls),
]
