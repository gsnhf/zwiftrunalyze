from flask import Flask, jsonify, request
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken

app = Flask(__name__)

client = Client(zwiftuser, zwiftpwd)
zwiftProfile = client.get_profile()
zwiftActivities = client.get_activity(zwiftProfile.profile["id"])
activitiesList = zwiftActivities.list()

# Beispiel-Daten (in der Praxis würdest du wahrscheinlich eine Datenbank verwenden)
data = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"name": "Item 2", "description": "This is item 2"},
}

# GET: Alle Elemente abrufen
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(activitiesList)

# GET: Ein bestimmtes Element abrufen
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
