# Bundestagsabgeordnete und Twitter



### Datenquellen

1. [Ergebnisse der Wahlkreise](https://bundeswahlleiter.de/bundestagswahlen/2021/ergebnisse.html) : Download der CSV-Datei mit tabellarischem Aufbau
2. [Umrisse der Wahlkreise](https://bundeswahlleiter.de/bundestagswahlen/2021/wahlkreiseinteilung/downloads.html): Download der generalisierten Shapefiles
3. [Twitter-Handles der MdBs](https://twitter.com/pollytix_gmbh/lists)

### Vorgehen

1. Umwandlung der Shapefiles in GeoJson mit [Aspose SHP -> GeoJSON](https://products.aspose.app/gis/conversion/shapefile-to-geojson)
2. Hochladen dieses GeoJSONs auf [mapshaper.org](mapshaper.org) und dort Verkleinerung
3. Erstelle eine *config.ini*-Datei mit deinen Twitter-Zugangsdaten im Format 
    
### TODO

- alles zu .env Files wechseln wegen bearer token
- import.py für Herunterladen der Listen
    - Funktion zum Austricksen der Pagination 
    - Speichern der einzelnen Parteien in Txt-Dateien
- fetch.py für Herunterladen der Tweets+ Nutzer-Daten