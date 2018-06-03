from django import forms
from .models import Ratings,Profile
from registration.forms import RegistrationFormUniqueEmail
from django_countries.fields import CountryField
from django.utils.timezone import now

'''
Aqui és on es defineixen els formularis.
Es creen les classes amb els camps desitjats. 
Les classes es creen en funció a un objecte, normalment en referència a un model.
'''

## Aquesta classe extèn de "RegistrationFormUniqueEmail" que hem importat del paquet registration.forms
## Només permet que s'enregistri un usuari amb un mail
class RegistrationForm(RegistrationFormUniqueEmail):

    '''
    first_name és un atribut, aquest atribut ha de fer referència a un atribut real del model.

    l'atribut first_name crida a un objecte de tipus CharField del paquet forms, a més ha de fer referència amb
    el tipus d'objecte que cridam al model, ja que sino no son el mateix no té cap sentit. (no funcionaria).
    
    a l'objecte li passam uns arguments determinats en funció del que vulguem
    '''

    first_name = forms.CharField(label='Nom : ', max_length=60, required=False)
    last_name = forms.CharField(label='Llinatges : ', max_length=90, required=False)
    birthday = forms.DateField(label='Aniversari : ', widget=forms.SelectDateWidget(years=range(1900, now().year + 1)))
    country = CountryField().formfield(label="País : ")

    ## Classe que li diu a Django quin model ha d'emprar i què ha d'emprar del model.
    ## Aquesta classe forma part de Django i defineix com ha de tractar les dades.
    ## https://docs.djangoproject.com/en/2.0/ref/models/options/
    class Meta:

        # Pren referència del model Profile
        model = Profile

        # Camps que ens ha de mostrar i que li passam al formulari
        fields = ['username','password1','password2','first_name','last_name','birthday','email','country']

## Aquesta classe extèn de ModelForm, pren com a referència un model per crear un formulari
class EditProfile(forms.ModelForm):

    # Atributs personalitzats
    # L'argument years crida a la funció now().year, que retorna l'any actual.
    # Com el rang no agafa l'any actual, se li ha de sumar 1
    birthday = forms.DateField(label='Aniversari : ',widget=forms.SelectDateWidget(years=range(1900, now().year + 1)))
    country = CountryField().formfield(label="País : ", required=False)

    class Meta:
        model = Profile
        fields = ['first_name','last_name','email','country','birthday','profile_image']
    
        
class CommentForm(forms.ModelForm):

    comment = forms.CharField(label='Comentari', required=True)
    rating = forms.DecimalField(label='Puntuació', max_digits=5, decimal_places=2, required=True)

    class Meta:
        model = Ratings
        fields = ('comment', 'rating', 'image')

