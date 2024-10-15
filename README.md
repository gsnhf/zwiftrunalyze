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

Um einen REST-Service in Python zu implementieren, kannst du verschiedene Frameworks verwenden. Eines der beliebtesten ist Flask, da es leichtgewichtig und einfach zu verwenden ist. Hier ist ein einfaches Beispiel, wie du einen REST-Service mit Flask einrichten kannst.

### Schritt 1: Flask installieren

Stelle sicher, dass du Flask installiert hast. Du kannst es mit pip installieren:

```bash
pip install Flask
```

### Schritt 2: Einen einfachen REST-Service erstellen

Hier ist ein einfaches Beispiel für einen REST-Service, der grundlegende CRUD-Operationen (Create, Read, Update, Delete) unterstützt:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Beispiel-Daten (in der Praxis würdest du wahrscheinlich eine Datenbank verwenden)
data = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"name": "Item 2", "description": "This is item 2"},
}

# GET: Alle Elemente abrufen
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# GET: Ein bestimmtes Element abrufen
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# POST: Ein neues Element erstellen
@app.route('/items', methods=['POST'])
def create_item():
    new_id = max(data.keys()) + 1
    new_item = request.json
    data[new_id] = new_item
    return jsonify(new_item), 201

# PUT: Ein vorhandenes Element aktualisieren
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = data.get(item_id)
    if item:
        item.update(request.json)
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# DELETE: Ein Element löschen
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data:
        del data[item_id]
        return jsonify({"message": "Item deleted"}), 204
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### Schritt 3: Den Service ausführen

Speichere den obigen Code in einer Datei, z.B. `app.py`, und führe sie aus:

```bash
python app.py
```

Der Server läuft standardmäßig auf `http://127.0.0.1:5000`.

### Schritt 4: API testen

Du kannst die API mit Tools wie **Postman** oder **curl** testen.

#### Beispiele:

- **Alle Elemente abrufen**:
  ```bash
  curl http://127.0.0.1:5000/items
  ```

- **Ein bestimmtes Element abrufen**:
  ```bash
  curl http://127.0.0.1:5000/items/1
  ```

- **Ein neues Element erstellen**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"name": "Item 3", "description": "This is item 3"}' http://127.0.0.1:5000/items
  ```

- **Ein Element aktualisieren**:
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"description": "Updated description"}' http://127.0.0.1:5000/items/1
  ```

- **Ein Element löschen**:
  ```bash
  curl -X DELETE http://127.0.0.1:5000/items/1
  ```

### Fazit

Das ist eine einfache Möglichkeit, einen REST-Service in Python mit Flask zu erstellen. Du kannst den Service weiter anpassen, um zusätzliche Funktionen hinzuzufügen, Fehlerbehandlung zu implementieren oder eine Datenbank wie SQLite oder PostgreSQL zu integrieren. Wenn du weitere Fragen hast, lass es mich wissen!