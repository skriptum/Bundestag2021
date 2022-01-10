# Bundestagsabgeordnete und Twitter



### Datenquellen

1. [Ergebnisse der Wahlkreise](https://bundeswahlleiter.de/bundestagswahlen/2021/ergebnisse.html) : Download der CSV-Datei mit tabellarischem Aufbau
2. [Umrisse der Wahlkreise](https://bundeswahlleiter.de/bundestagswahlen/2021/wahlkreiseinteilung/downloads.html): Download der generalisierten Shapefiles
3. [Twitter-Handles der MdBs](https://twitter.com/pollytix_gmbh/lists)

### Vorgehen

1. Umwandlung der Shapefiles in GeoJson mit [Aspose SHP -> GeoJSON](https://products.aspose.app/gis/conversion/shapefile-to-geojson)
2. Hochladen dieses GeoJSONs auf [mapshaper.org](mapshaper.org) und dort Verkleinerung
3. Erstelle eine *config.ini*-Datei mit deinen Twitter-Zugangsdaten im Format 
    
### GOALS

Graphics showing

### Was gerade im BT abgeht (generell)
- meistgenutzte Hashtags
- erfolgreichster Tweet
- heutige Anzahl Tweets
- Vergleich aller Parteien Followers (treemap)

### persönlichs Twitter Profil
- Platzierung Follower, etc
- Kategorie (retweeter, meinung, antworter, mischung)

### Vergleichsportal
Vergleich von Kategorien (Anzahl Tweets, Follower, ...)
- als Siegertreppchen
- auf Karte angewendet

## HEROKU SOLUTION
https://medium.com/@shalandy/deploy-git-subdirectory-to-heroku-ea05e95fce1f