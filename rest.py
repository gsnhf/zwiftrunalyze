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
