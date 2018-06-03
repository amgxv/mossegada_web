from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

# https://tutorial-extensions.djangogirls.org/en/homework_create_more_models/

'''
https://docs.djangoproject.com/en/2.0/topics/db/models/
Aqui és on cream els models, aquests models defineixen com es guardaràn les nostres dades.
Cada classe defineix una taula de la base de dades, cada atribut és una columna de la base de dades.

Tot el que es defineix aqui, necessita crear una migració (crea el codi SQL)
i aplicar la migració (Aplica els canvis a la base de dades)
'''

## Classe que extèn de Model. Defineix un model.
class TypeRestaurants(models.Model):

    # Atributs, i quin tipus tenen
    id = models.AutoField(primary_key=True)
    typeR = models.CharField(max_length=60)

    # Métode de la classe, defineix quin és el valor del __str__
    # __str__ és un mètode màgic de Python que retorna la representació en string del objecte, facilita la seva interpretació.
    def __str__(self):
        return self.typeR 

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    address  = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    website = models.CharField(max_length=300)
    phone = models.CharField(max_length=30)
    typeR_fk = models.ForeignKey(TypeRestaurants, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images', blank=True)
      
    def __str__(self):
        return self.name
    
class Ratings(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.DecimalField(max_digits=5,decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    ## Per defecte tots els comentaris son aprovats, aquest camp pot quedar pendent per un futur.
    approved = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images_user_ratings/%Y/%m/%d/', blank=True)
    rest_fk = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return 'Comment by ' + '[' + str(self.user_fk) + ']' + ' on ' + '[' + str(self.rest_fk) + ']'

class Profile(AbstractUser):
    country = CountryField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='images_user_profile/%Y/%m/%d/', blank=True)

    def age(self):
       import datetime
       return int((datetime.date.today() - self.birthday).days / 365.25  )
