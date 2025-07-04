from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    period = request.args.get("period")
    if not period:
        return jsonify({"error": "No period provided"}), 400

    try:
        response = requests.get("https://www.goaok.com/wingo1min")
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table tr")[1:6]
        last_results = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                number = cols[1].text.strip()
                bs = cols[2].text.strip()
                last_results.append((number, bs))

        big_count = sum(1 for _, bs in last_results if bs == "Big")
        small_count = 5 - big_count

        if big_count > small_count:
            prediction = "Small"
        elif small_count > big_count:
            prediction = "Big"
        else:
            prediction = "Big"

        return jsonify({
            "period": period,
            "prediction": prediction,
            "last_5": last_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
