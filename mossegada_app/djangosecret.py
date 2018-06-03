"""
https://programadorwebvalencia.com/como-generar-un-secret-key-en-django/

Pseudo-random django secret key generator.
- Does print SECRET key to terminal which can be seen as unsafe.
"""

import string
import random
#import fileinput

# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, 
string.punctuation]).replace('\'', '').replace('"', '').replace('\\', 
'')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in 
range(50)])

with open("RestaurantsProject/settings.py") as f:
	newText=f.read().replace('PLEASEGENERATEDJANGOSECRETKEY', SECRET_KEY)

with open("RestaurantsProject/settings.py", "w") as f:
	f.write(newText)

print(SECRET_KEY)
