# mossegada_web
[![Build Passing](https://github.com/dwyl/repo-badges/blob/master/svg/build-passing.svg)](https://hub.docker.com/r/amgxv/mossegada_web/)


Projecte Final del FP Administració de Sistemes Informàtics en Xarxa

---

## [DEMO](https://mossegada.amgxv.com)


## Com deplegar el projecte?

1. Edita el fitxer __traefik.toml__ i afegeix el teu correu electrònic. Aquest fitxer es troba a la carpeta traefik o traefik-swarm en funció del que vulguis desplegar.  

```
...
# Email address used for registration
email = "'MAIL'"
...
```

2. Edita el fitxer docker-compose.yml o docker-compose-swarm.yml en funció del que vulguis desplegar. A aquests fixers, modifica les variables d'entorn corresponents amb el que vulguis.  

- __Postgres__ : Es definieixen el nom de la base de dades, l'usuari i contrasenya que tindrà la base de dades.
```
    environment:
      - POSTGRES_DB='DATABASE'
      - POSTGRES_USER='USERNAME'
      - POSTGRES_PASSWORD='PASSWORD'
```
- __NGINX__ : Cal definir el nom de host. El domini al qual ha de responre.
```
      labels:
        ...
        - "traefik.frontend.rule=Host:'HOST'"
        ...
```
- __SMTP__ : Es defineix el nom de domini del mail i l'usuari i contrasenya per SMTP
```
    environment:
      - maildomain='DOMAIN'
      - smtp_user='USERNAME:PASSWORD'
```
- __Django__ : Es defineix com ha de accedir a les dades. Cal passar les credencials del servidor Postgres i del SMTP. A més del host de la web i l'API Key pels mapes de Google.

```
    environment:
      - DB_NAME='DATABASE'
      - DB_USER='USERNAME'
      - DB_PASS='PASSWORD'
      - DB_HOST='HOSTNAME'
      - DB_PORT='PORT'
      - SMTP_HOST='SMTP'
      - SMTP_USER='USER'
      - SMTP_PASS='PASSWORD'
      - WEB_HOST='HOST'
      - GMAPS_API='API_KEY'
```

3. Desplega el projecte.  
En cas de desplegar-ho amb Docker Compose, fora Docker Swarm basta amb executar ```docker-compose up ``` al directori on estigui el fitxer compose.  
Si es desplega amb Docker Swarm, cal fer-ho de la següent manera :  
-  Si no hem iniciat un swarm...  ```docker swarm init```
-  Per desplegar la configuració al swarm : ```docker stack deploy -c docker-compose-swarm.yml``` 
- Un cop executat el següent, tot començarà a agafar forma i hauriem de tenir el nostre desplegament fet al domini escollit.



