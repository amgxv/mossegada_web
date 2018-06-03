"""
WSGI config for RestaurantsProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/


WSGI is the Web Server Gateway Interface
WSGI[1] is not a server, a python module, a framework, an API or any kind of software. It is just an interface specification by which server and application communicate. Both server and application interface sides are specified in the PEP 3333. If an application (or framework or toolkit) is written to the WSGI spec then it will run on any server written to that spec.

WSGI permet la inteacció entre el servidor web i l'aplicació
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RestaurantsProject.settings")

application = get_wsgi_application()
