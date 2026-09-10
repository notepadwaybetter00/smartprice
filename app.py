import json
import os

from flask import Flask, jsonify, render_template, request

from sample_data import build_catalog, enrich, search_products

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder="static")

catalog = build_catalog()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    results = [enrich(p) for p in search_products(catalog, query)]
    return jsonify({"products": results, "count": len(results)})


@app.route("/api/catalog")
def api_catalog():
    return jsonify({"names": [p["name"] for p in catalog]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "1") == "1")