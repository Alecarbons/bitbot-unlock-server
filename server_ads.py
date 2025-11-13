from flask import Flask, request
import json
import os

app = Flask(__name__)

DATA_FILE = "ads_credits.json"

# Carica o crea file credito
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/unlock", methods=["GET"])
def unlock():
    uid = str(request.args.get("uid"))

    if not uid:
        return "User ID missing", 400

    data = load_data()
    user = data.get(uid, {"views": 0, "days": 0})

    # --- HTML SAFE, NO BROKEN QUOTES ---
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BitBot Unlock</title>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial; text-align:center;">
        <h2>BitBot — Guarda Ads per Sbloccare Giorni</h2>
        <p>Utente: {uid}</p>
        <p>Ads viste: {user['views']} / 5</p>

        <button onclick="window.location='/watch?uid={uid}'"
                style="padding:20px; font-size:22px; margin-top:20px;">
            Guarda Pubblicità
        </button>
    </body>
    </html>
    """

    return html


@app.route("/watch", methods=["GET"])
def watch():
    uid = str(request.args.get("uid"))
    data = load_data()

    user = data.get(uid, {"views": 0, "days": 0})

    user["views"] += 1

    # Se 5 ads → 1 giorno
    if user["views"] >= 5:
        user["views"] = 0
        user["days"] += 1

    data[uid] = user
    save_data(data)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BitBot - Grazie!</title>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial; text-align:center;">
        <h2>Grazie!</h2>
        <p>Hai visto un ad.</p>
        <p>Ads viste: {user['views']} / 5</p>
        <p>Giorni accumulati: {user['days']}</p>

        <a href="/unlock?uid={uid}"
           style="font-size:20px; display:inline-block; margin-top:20px;">
            Torna indietro
        </a>
    </body>
    </html>
    """

    return html


@app.route("/")
def home():
    return "BitBot Unlock Server — Online"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
