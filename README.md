# zwiftrunalyze
This is a fork of [zwiftrunalyze](https://github.com/pnposch/zwiftrunalyze) from [pnposch](https://github.com/pnposch). I fixed some bugs.

The original program was not working for me. 

Download FIT files from [Zwift](www.zwift.com) or [MyWhoosh](www.mywhoosh.com) and upload to runanalyze. Simple as that.

[Zwift](www.zwift.com) and [MyWhoosh](www.mywhoosh.com) are popular virtual reality worlds for cyclists and runners.

[Runalyze](www.runalyze.com) is a privacy-friendly training log with extensive functionality (and its free!)

## Prequisites
Install requirements with:

``` sh
pip install -r requirements.txt
```
to include the few other (standard) packages needed.

## Alternatively use the Docker config below.

or include the few other (standard) packages needed:
``` sh
pip install -r requirements.txt 
```

- add data directory to your folder ``` mkdir data ```

- Rename ```zrconfig.py.example``` to ``` zrconfig.py ``` and proceed to config (no worries only three infos needed)


## Configure
Add your zwift username, zwift password and obtain a token for runanalyze (https://runalyze.com/settings/personal-api) and entere it too in the header of main.py and you are good to go. 

FIT files are downloaded into /data and pushed to runanalyze, once downloaded there are not requested a second time. Furthermore Zwift info is saved in a JSON file.

## Docker
Use Docker Image with local mounts of data/ and zrconfig.py/

``` sh
docker-compose up -d --build
```

To recreate the image 

``` sh
docker-compose up -d --build --force-recreate
```

Then start zwift import with

``` sh
docker exec zwiftrunalyze_app_1 python3 main.py
```

or MyWhoosh import with 

``` sh
docker exec zwiftrunalyze_app_1 python3 mywhoosh.py
```

which can be added to the host system's crontab

``` sh
crontab -e
```

e.g. run every evening at 22:30h:

``` sh
30 22 * * * docker exec zwiftrunalyze_app_1 python3 main.py
```

## Run locally
Simple: 

``` sh
python3 main.py
``` 
or 

``` sh
python3 mywhoosh.py
``` 
Make the file executable: 

``` sh
chmod +x main.py
```
and

``` sh
./main.py
```
.

Optional argument: Download only after date:
``` sh
python3 main.py YYYY.MM.DD
```
will skip any zwift acitivies ended before YYYY-MM-DD
s

## REST

Um einen Python REST-Service mit Docker Compose zu hosten, kannst du die folgenden Schritte ausführen. Wir verwenden ein einfaches Beispiel mit Flask, um den Prozess zu demonstrieren.

### Schritt 1: Erstelle die Projektstruktur

Erstelle ein Verzeichnis für dein Projekt und lege die folgenden Dateien an:

```
my_flask_app/
├── app.py
├── requirements.txt
└── docker-compose.yml
```

### Schritt 2: Erstelle die Flask-Anwendung

**`app.py`:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"items": ["item1", "item2", "item3"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
```

### Schritt 3: Erstelle die Anforderungen

**`requirements.txt`:**

```
Flask==2.0.3
```

### Schritt 4: Erstelle die Docker-Compose-Konfiguration

**`docker-compose.yml`:**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5005:5005"
```

### Schritt 5: Erstelle das Dockerfile

Erstelle eine Datei mit dem Namen `Dockerfile` im gleichen Verzeichnis:

**`Dockerfile`:**

```dockerfile
# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Anforderungen installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung kopieren
COPY app.py app.py

# Anwendung starten
CMD ["python", "app.py"]
```

### Schritt 6: Baue und starte die Anwendung mit Docker Compose

Navigiere in dein Projektverzeichnis `my_flask_app` und führe den folgenden Befehl aus:

```bash
docker-compose up --build
```

- `--build`: Baut die Images neu, falls Änderungen vorgenommen wurden.

### Schritt 7: Teste den REST-Service

Sobald der Container läuft, kannst du den REST-Service testen, indem du im Browser oder mit einem Tool wie `curl` oder Postman auf die URL zugreifst:

```bash
curl http://localhost:5005/items
```

### Schritt 8: Stoppe die Anwendung

Um die Anwendung zu stoppen, kannst du im Terminal `Ctrl + C` drücken oder den folgenden Befehl ausführen:

```bash
docker-compose down
```

### Fazit

Mit diesen Schritten hast du einen Python REST-Service mit Docker Compose erfolgreich gehostet. Du kannst die Anwendung weiter anpassen, zusätzliche Dienste hinzufügen oder die Konfiguration nach Bedarf erweitern. Wenn du Fragen hast oder Unterstützung benötigst, lass es mich wissen!