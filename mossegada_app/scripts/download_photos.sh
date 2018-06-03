#!/bin/bash

# Gets the folder path
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

## Download the files
wget -i "$SCRIPTPATH/photolinks"

## Rename the files
mv arroz-de-bacalao-i.jpg canprim-1.jpg
mv bottega-birthdays.jpg bottegabay1.jpg
mv dorf-bar-und-restaurant.jpg barnou1.jpg
mv eingang.jpg placagalilea.jpg
mv fachada-de-nuestro-local.jpg perla1.jpg
mv fantasticas-hamburguesas.jpg brox1.jpg
mv filename-img-3335-jpg.jpg canpaco.jpg
mv getlstd-property-photo.jpg cansito1.jpg
mv la-facade-de-l-etablissement.jpg barandaluz.jpg
mv la-vila.jpg lavila.jpg
mv photo0jpg.jpg therose.jpg
mv photo0jpg.jpg.1 500grados.jpg
mv photo2jpg.jpg primo.jpg
mv photo2jpg.jpg.1 horapa.jpg
mv placa-verge-del-miracle.jpg llimona.jpg
mv puerta-principal.jpg norte.jpg
mv restaurante-es-cruce.jpg cruce.jpg
mv terraza-exterior-con.jpg tasteindia.jpg

## Copy all .jpg to media/images folder
mv *.jpg -t ../web_restaurants/media/restaurant_images