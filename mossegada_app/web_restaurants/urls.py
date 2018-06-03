from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from . import views
from rest_framework import routers

'''
Despatxador d'URLs. S'encarrega de gestionar/encaminar les nostres URLs, en funció del que li diguem.
Dades adicionals:

r = Raw String. 
Tot el que s'escrigui dedins és el que hi serà a l'string. 
Això ens permet emprar expressions regulars (regex).
'''

'''
Router
------
És part del Django Rest Framework.
S'encarrega de crear les rutes a l'API, a més d'afegir el seu sistema de templating per defecte.
Pots crear un router personalitzat, amb estils personalitzats...
'''

# Variable per cridar al DefaultRouter
router = routers.DefaultRouter()
# Registra les rutes. Se li passen dos arguments, la ruta en qüestió, i la vista.
router.register(r'restaurants', views.RestaurantAPIView)
router.register(r'ratings', views.RatingsAPIView)


urlpatterns = [
    # Path a la pàgina principal
    path(r'', views.home, name='home'),
    # Path a un restaurant concret. Filtra per id de restaurant.
    path(r'restaurant/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    # Path a la API, s'inclouen les URL's del router.
    path(r'api/', include(router.urls), name='restapi'),
    # Path a la pàgina AJAX
    path(r'ajax/', views.ajax , name="ajax"),
    # Path al backend del django-registration-redux.
        # Inclou els paths que té el plugin.
        # Aqui s'explica. https://django-registration-redux.readthedocs.io/en/latest/quickstart.html?highlight=.default.urls#setting-up-urls
        # I aqui es poden descarregar els templates https://github.com/macropin/django-registration/tree/master/registration/templates/registration
    path(r'accounts/', include('registration.backends.default.urls')),
    # Path per el perfil de l'usuari
    path(r'profile/<username>/', views.get_user_profile),
    # Path al formulari per editar el perfil
    path(r'profile/<username>/editprofile/', views.editprofile),
    # Path als arxius estàtics (es defineix el path real al arxiu)
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
