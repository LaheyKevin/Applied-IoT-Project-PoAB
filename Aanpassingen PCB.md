# Aanpassingen PCB

## Main board
### Power supply
Supply nodig van verschillende spanningen:

- 12V
- 5V
- 3V3

De 12V en 5V spanningen komen rechtstreeks van de solar controller
De 3V3 spanning komt van het MKR board -> is enkel voor GPS en 3 lichtsensoren


5V komt van USB-terminal -> power connection maken naar PCB

### Interface LED-controlboard
Wisselen van 3 rijen van 2 connectoren naar 1 rij van 6 connectoren


### I²C interface toevoegen voor uitbreidbaarheid

## LED-controlboard
### Current Regulator
De current regulator die er momenteel op staat, geeft een veel te lage stroom. Dit onderdeel moet dus worden vervangen

->Current regulator is vervangen door een spanningsregelaar gebaseerd op een LM317. We hebben namelijk gemerkt dat de bakenlichten een ingebouwde spanningsgestuurde begrenzer heeft. Het is dus genoeg om enkel de spanning te regelen.

### Connectors
- Aanpassen van simpele, open pin headers naar schroefconnectoren 
- Aanpassen van 3x2-pin connectoren naar 1x6-pin connector
