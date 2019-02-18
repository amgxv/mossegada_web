from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
from .models import Restaurant,Ratings,Profile
from .serializers import RestaurantSerializer,RatingSerializer
from .forms import CommentForm,EditProfile
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings


'''
Una vista, és una funció que agafa una petició HTTP i la retorna en resposta. Aquesta resposta pot ser una pàgina
en HTML, errors...
Les vistes contenen la lógica necessaria per respondre amb X.
El codi pot estar on sigui, mentre que estigui al teu path de Python.

https://docs.djangoproject.com/en/2.0/topics/http/views/
'''

## Funció per la vista de la pàgina principal
@cache_page(60 * 15)
def home(request):
    ## Variable amb la plantilla a renderitzar
    template = 'web_restaurants/home.html'

    ## Variable amb la query per retornar els restaurants. Aquesta té un filtre per obtenir els més valorats primer.
    restaurant_list = Restaurant.objects.annotate(avg_rating=Coalesce(Avg('ratings__rating'), Value(0.00))).order_by('-avg_rating').distinct()

    ## Variable que transforma a valor enter. Obté el valor paràmetre "res", si no obté res per defecte és 6. Son els restaurants a mostrar per pantalla.
    queryfilter = int(request.GET.get('res', 6))

    ## Variable que obté el valor del paràmetre "q". Serveix per fer la cerca
    query = request.GET.get("q")

    ## Si hi ha cerca, retorna la llista de restaurants filtrada. Obté per nom i per direcció.
    if query:
        restaurant_list = restaurant_list.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
            ).distinct()

    # Variable per cridar al Paginator, se li passen dos arguments, la llista de restaurants a paginar, i el número de resultats que ha de mostrar
    paginator = Paginator(restaurant_list, queryfilter)

    ## Variable que transforma a valor enter. En cas de que obtengui valor del paràmetre 'page' l'agafa, sino per defecte és 1.
    page = int(request.GET.get('page', '1'))
    ## Variables a 0
    next_page = None
    prev_page = None

    ## Si la pàgina actual + 1 és menor al numero de pàgines actuals
    ## La variable per la pàgina següent tindrà el valor "/?page={page + 1}"(pàgina actual + 1) "&res={queryfilter}" (filtre de restaurants)
    if page + 1 < paginator.count:
        next_page = f'/?page={page + 1}&res={queryfilter}'

    ## Si la pàgina actual -1 és major a 0
    ## La variable per pàgina anterior tindrà el valor "/?page={page - 1}" (pàgina actual -1) "&res={queryfilter}" (filtre de restaurants)
    if page - 1 > 0:
        prev_page = f'/?page={page - 1}&res={queryfilter}'

    ## En cas de que hi hagi una cerca de restaurants...
    if query:
        ## S'empren les variables anteriors, ja que també comprova si hi ha pàgina següent o no.
        ## En cas de que hi hagi pàgina següent, afegeix el valor next_page i el valor de la cerca.
        ## En cas contrari, només farà la cerca i no paginarà perque no té res a paginar
        next_page = f'{next_page}&q={query}' if next_page is not None else f'?q={query}'
        ## En cas de que hi hagi anterior següent, afegeix el valor prev_page i el valor de la cerca.
        ## En cas contrari, només farà la cerca i no paginarà perque no té res a paginar
        prev_page = f'{prev_page}&q={query}' if prev_page is not None else f'?q={query}'

    # Variable que crida al paginador per obtenir els resultats
    # Aquesta se li passa com a context de la pàgina
    restaurants = paginator.get_page(page)

    # Context de la pàgina, paràmetres que se li passen, així es pot renderitzar mitjançant templating.
    # També se li passen ses variables per avançar i retrocedir pàgina
    context = {'restaurants': restaurants, 'next_page': next_page, 'prev_page': prev_page}

    #En cridar la funció ha de retornar la petició, la plantilla a renderitzar i el context
    return render(request, template, context)

## Funció per la vista un restaurant concret. A més de la petició també se li passa la ID del restaurant concret.
@cache_page(60 * 15)
def restaurant(request, restaurant_id):

    # Plantilla a renderitzar
    template = 'web_restaurants/restaurant.html'
    GOOGLE_MAPS_API = settings.GOOGLE_MAPS_API

    # Intenta obtenir la informació d'un restaurant en concret, si no pot, tira un 404
    try:
        ## Query de restaurants, filtra per id.
        restaurant_q = Restaurant.objects.get(id=restaurant_id)
        ## Variable per filtrar els comentaris
        ## En cas de voler filtrar per comentaris aprovats o no, es qüestió de modificar aquesta query.
        ## Ara només mostra els comentaris que estàn aprovats, però tots estàn aprovats per defecte.
        comments_q = Ratings.objects.all().filter(rest_fk=restaurant_id, approved=True).order_by('-date')
        ## Variable amb la query per mostrar la valoració mitjana del restaurant
        avg_rat = Ratings.objects.all().filter(rest_fk=restaurant_id).aggregate(Avg('rating'))

    except Restaurant.DoesNotExist:
        raise Http404("NORRR")

    # Variable amb el filtre de comentaris
    commentfilter = 6
    # Variable per cridar al paginator, amb dos arguments, la llista de comentaris i el filtre
    paginator = Paginator(comments_q, commentfilter)

    page = int(request.GET.get('c', '1'))
    next_page = None
    prev_page = None

    # Si hi ha pàgina següent o anterior, cambia el resultat de la variable
    if page + 1 < paginator.count:
        next_page = f'/restaurant/{restaurant_id}/?c={page + 1}'

    if page - 1 > 0:
        prev_page = f'/restaurant/{restaurant_id}/?c={page - 1}'

    comments = paginator.get_page(page)

    # Si hi ha una petició POST, demana el POST i els arxius.
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        # Si el formulari és vàlid, agafa el comentari, afegeix quin és el restaurant i l'usuari que ha fet el comentari, i el guarda.
        if form.is_valid():
            comment = form.save(commit=False)
            comment.rest_fk = restaurant_q
            comment.user_fk = request.user
            comment.save()
            # Redirecció al div dels comentaris (per no haver de baixar pàgina)
            return redirect(request.path + '#comments')
    # En cas contrari posa el formulari a 0
    else:
        form = CommentForm()

    # Context de la pàgina, paràmetres que se li passen, així es pot renderitzar mitjançant templating i interactuar amb el formulari.
    # També se li passen ses variables per avançar i retrocedir pàgina
    context = {
        'restaurant_q': restaurant_q,
        'comments': comments,
        'avg_rat': avg_rat,
        'next_page': next_page,
        'prev_page': prev_page,
        'form': form,
        'google_maps_api': GOOGLE_MAPS_API
        }

    #En cridar la funció ha de retornar la petició, la plantilla a renderitzar i el context
    return render(request, template, context)

# Funció per obtenir el perfil de l'usuari, se li passa el nom d'usuari per obtenir el perfil.
@login_required
def get_user_profile(request, username):

    # Variable per cercar l'usuari
    user = Profile.objects.get(username=username)

    # Retorna la renderització de la vista del perfil de l'usuari
    return render(request, 'web_restaurants/userprofile.html', {"user": user})



# Funció per editar el perfil de l'usuari.
def editprofile(request, username):

    # Si es fa un POST
    if request.method == 'POST':
        # Es demana el POST, els Arxius, i el Usuari (només pot fer canvis a l'usuari loguejat)
        form = EditProfile(request.POST, request.FILES, instance=request.user)

        # Si el formulari és vàlid, el guarda i el redirigeix al seu perfil
        if form.is_valid():
            form.save()
            return redirect('/profile/' + username + '/')

    # Si no es fa cap petició POST, genera el formulari amb les dades actual de l'usuari
    else:
        form = EditProfile(instance=request.user)
        # Context/Arguments que se passen per interactuar amb el formulari
        args = {'form': form}
        # Renderitza la pàgina d'edició del perfil (formulari i tot)
        return render(request, 'web_restaurants/editprofile.html', args)

# Decorador per obliga a l'usuari a fer login
@login_required
# Funció per la pàgina AJAX
def ajax(request):

        return render(request, 'web_restaurants/ajax.html')

# Classe per la vista dels restaurants a la API.
# Extèn de viewsets.ReadOnlyModelViewSet, així només permet lectura, i per tant no es pot fer POST
class RestaurantAPIView(viewsets.ReadOnlyModelViewSet):

    # Query que ha de realitzar
    queryset = Restaurant.objects.all()

    # Classe del Serialitzador
    serializer_class = RestaurantSerializer

    # Classes per autenticació
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    # Permissos de les classes. Demana autenticació.
    permission_classes = (IsAuthenticated,)

    # Funció per la Query, fa que es retornin els restaurants d'una manera concreta. (També filtra els de major puntuació)
    def get_queryset(self):
        return Restaurant.objects.annotate(avg_rating=Coalesce(Avg('ratings__rating'), Value(0.00))).order_by('-avg_rating').distinct()

# Classe per la vista de les valoracions a la API.
# Extèn de viewsets.ReadOnlyModelViewSet, així només permet lectura, i per tant no es pot fer POST
class RatingsAPIView(viewsets.ReadOnlyModelViewSet):

    # Query que s'ha de realitzar
    queryset = Ratings.objects.all()

    # Classe del Serialitzador
    serializer_class = RatingSerializer

    # Classes per autenticació
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    # Permissos de les classes. Demana autenticació i ser admin.
    permission_classes = (IsAuthenticated, IsAdminUser)
