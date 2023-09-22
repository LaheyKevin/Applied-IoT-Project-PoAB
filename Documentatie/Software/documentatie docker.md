# Docker documentatie

## Docker in Linux
---
Als eerste stap moet Docker geinstalleerd worden op de linux-server. Docker dient om verschillende services in hun eigen environment te laten runnen genaamd een container. Deze services kunnen niet aan de fysieke hardware en andere containers komen. Ze leven dus een beetje in hun eigen wereld, vandaar dat ze containers genoemd worden.

## Containers
---
De containers die gebruikt worden, zijn Portainer, Nginx, Influxdb, grafana en Flask.
Portainer is een interface voor Docker, hierin kunnen alle containers, Docker-netwerken, images en veel meer worden beheerd. Nginx wordt gebruikt om aan reverse proxy te doen. Hierdoor hoef je geen poortnummer te plaatsen achter het DNS maar een duidelijke alias, bv. '**/database**' refereerd naar '**:8086**'. Om de data op te slaan en op te vragen wordt gebruik gemaakt van Influxdb. Deze loopt ook weer in een container naast de rest. Als laatste gebruiken we Flask. Flask wordt gebruikt als interface van het project. Dit werkt wat moeilijker omdat de Flask-app eerst ontwikkeld moet worden, vervolgens moet er een image van gemaakt worden en dan pas kan Docker deze image gebruiken om te deployen.

## Installatie stappen
---
### 1. Docker
- Als eerste wordt linux geupdate met `sudo apt-get update` vervolgens downloaden we een 	aantal librarys met `sudo apt-get install ca-certificates curl gnupg`. 

- Je maakt een map voor keyrings aan met `sudo install -m 0755 -d /etc/apt/keyrings`. 				Daarna wordt de GNU Privacy Guard (GPG) geinstalleerd met het commando `curl -fsSL 		https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/			docker.gpg` en zorgen ervoor dat het bestand overal gelezen kan worden `sudo chmod 			a+r /etc/apt/keyrings/docker.gpg`.

- Als laatste slaag je de repository op in de Apt sources met `echo \"deb [arch="$(dpkg --			print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/			linux/ubuntu \ "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \ sudo tee 	/etc/apt/sources.list.d/docker.list > /dev/null sudo apt-get update`.

- Alle nodige bestanden zijn nu beschikbaar om Docker te installeren, dit kan met het volgende commando `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`. Om te testen kan je de hello-word container laten runnen `sudo docker run hello-world`.

### 2. Docker-compose
- Als alle stappen voor Docker juist gebeurd zijn krijg je met `docker compose version` te zien welke versie er op de Linux staat. Dan is niet nodig om Docker-compose te installeren. Als dat wel moet gebruik je deze commando `sudo apt-get install docker-compose-plugin`.

- Om Docker-compose effectief te gebruiken moet je een *docker-compose.yaml* aanmaken met `nano docker-compose.yaml`. Bovenaan zet je alvast
```
version: "0.1"
```

In deze file zet je alle containers met, zo nodig, instellingen die je aangepast wilt hebben. Dit kunnen zijn, poorten, custom images, restart procedures, ... De installaties van de gebruikte containers komen later aan bod.

### 3. Portainer
- Portainer wordt gebruikt om de Docker installatie te kunnen beheren via een interface. Deze installatie wordt ook in een container geplaatst. Om dit te installeren plaats je het volgende in de *docker-compose.yaml*.

```
services:
 portainer:
    container_name: portainer
    image: portainer/portainer-ce
    restart: always
    stdin_open: true
    tty: true
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /opt/portainer:/data
```


### 4. Nginx
- Nginx wordt gebruikt om aan reverse proxy te doen. Hierdoor moet je niet meer zoeken naar de poort, bv. ***172.50.0.4:6000*** kan je instellen als***172.50.0.8/database*** of, als je een dns hebt, ***'websitedns'/database***. Om dit te installeren plaats je het volgende in de *docker-compose.yaml*.

```
 nginx:
    container_name: nginx
    image: nginx
    ports:
      - "80:80"
    restart: always
```

- Om de proxy in te stellen kopieer je de *default.conf* uit de Nginx configuratie in een directory naar wens. Dit doe je met `sudo docker cp nginx:/etc/nginx/conf.d/default.conf default.conf`. Vervolgens gebruik je `nano default.conf`om het bestand aan te passen. De structuur die in dit bestand gebruikt moet worden is als volgt.

```
server {
    listen       80;
    listen  [::]:80;
    server_name localhost;

    #access_log  /var/log/nginx/host.access.log  main;


-- Met intern ip van een Docker-netwerk--

    location /database {
        proxy_pass http://172.50.0.4:6000;
    }

-- Of met het host-ip --

    location /flask {
        proxy_pass http://192.168.0.70:5000;
    }
```

- Als je alles er in hebt staan kopieer je dit bestand terug naar de Nginx config met `sudo docker cp default.conf nginx:/etc/nginx/conf.d/`. Voor de zekerheid doe je `sudo docker exec nginx nginx -t`, dit test of de configuratie klopt. Als laatste moet de configuratie van Nginx opnieuw opgestart worden. Dit kan met `sudo docker exec nginx nginx -s reload`.

### 5. Influxdb


### 6. Grafana
### 7. Flask

Om alle containers te installeren run je het commando `docker-compose up -d`. LET OP! Dit werkt alleen als je je bevind in de directory waar de *docker-compose.yaml* staat. Om in de interface van bv. Portainer te komen zoek je naar ***'ip-addres':9000*** zoals bv. ***172.50.0.8:9000***.


## Bronnen

https://docs.docker.com/engine/install/ubuntu/
https://blog.logrocket.com/build-deploy-flask-app-using-docker/