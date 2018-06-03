from rest_framework import serializers
from .models import Restaurant, TypeRestaurants, Ratings, Profile
from django.contrib.auth.models import User

#ModelSerializer
#It will show you the information relevant to your model, also has the functionality to create new models, and update the models.

'''
http://www.django-rest-framework.org/api-guide/serializers/

Classe que s'encarrega de renderitzar les querys en JSON, XML o altres.

Els serialitzadors també proporcionen la deserialització, permet que les dades analitzades 
es converteixin de nou en tipus complexes després de la validació de les dades entrants.

El seu funcionament és senzill, similar al dels models.
Podem definir vistes pròpies o basades en funció als models.

Aqui s'empren en funció als models creats.
'''

## Classe que extèn de serializers.ModelSerializer. S'encarrega de serialitzar un model
class TypeRestaurantsSerializer(serializers.ModelSerializer):

    # Diu com es tracten les dades
    class Meta:
        # Definim el model
        model = TypeRestaurants
        # Definim els camps que volem treure
        fields = ('typeR',)

'''
Per obtenir les relacions, primer s'ha de serialitzar "el model de la foreign key", després tu pots
per la crida a aquesta classe serialitzadora des d'un atribut.
'''

class RestaurantSerializer(serializers.ModelSerializer):

    # Atribut que crida a la classe TypeRestaurantsSerializer per obtenir el tipus de Restaurant, pren com a referència la mateixa classe
    typeR_fk = TypeRestaurantsSerializer(many=False, read_only=True)
    # Atribut de tipus FloatField
    avg_rating = serializers.FloatField()

    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'avg_rating', 'latitude',
                  'longitude', 'website', 'phone', 'image', 'typeR_fk',)


## Aquestes dues classes serialitzen el nom d'usuari i el nom del restaurant
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username',)

class RestaurantName(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name',)


class RatingSerializer(serializers.ModelSerializer):

    # No puc fer referència directa a RestaurantSerializer perque aqui no s'especifica 'avg_rating'
    rest_fk = RestaurantName(many=False, read_only=True)
    user_fk = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Ratings
        fields = ('rest_fk', 'user_fk', 'rating',
                  'comment','image', 'date', 'approved')
