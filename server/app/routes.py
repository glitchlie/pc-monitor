from app import app
from flask import render_template, request, jsonify

from time import time
import sys
sys.path.append("..")

from redis_client import Redis


redis_client = Redis()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/getData")
def getData():
    client_name = request.args.get("clientName")
    hardware = request.args.get("hardware")
    indicator = request.args.get("indicator")
    start_idx = request.args.get("startIdx")
    end_idx = request.args.get("endIdx")
    
    list_name = "%s_%s_%s" % (client_name, hardware, indicator)
    data = {"data": redis_client.fetch_records(list_name, start_idx, end_idx)}
    return jsonify(data)


@app.route("/getDataIncr")
def getDataIncr():
    client_name = request.args.get("clientName")
    hardware = request.args.get("hardware")
    indicator = request.args.get("indicator")
    start_score = request.args.get("startScore")
    end_score = request.args.get("endScore")
    
    list_name = "%s_%s_%s" % (client_name, hardware, indicator)
    data = {"data": redis_client.fetch_increment(list_name, start_score, end_score)}
    #if not data["data"]:
    #    data["data"] = [[ts, None] for ts in range(start_score, end_score)]

    #print(data)
    return jsonify(data)
