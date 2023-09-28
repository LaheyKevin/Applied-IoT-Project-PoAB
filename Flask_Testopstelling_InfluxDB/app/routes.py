# logica van de toepassing

from flask import render_template, flash, redirect, url_for, request, Flask
from werkzeug.urls import url_parse
from app import app
from app.ttn2 import create_downlink, create_downlink_all
#import app.ttn

#INFLUXDB
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
bucket = "TestOpstellingBaken"
token = "jw-O_3q5SVuqGDN2jjWtvtRP3q8f80DXX0mQyqozDbFVA203KyWLlwxelp8SCY1lzEUNRwJc_e8lZzkFg8o93Q=="
org = "AP"
url = "http://127.0.0.1:8086"
DBclient = influxdb_client.InfluxDBClient(url=url,token=token,org=org)
write_api = DBclient.write_api(write_options=SYNCHRONOUS)
read_api = DBclient.query_api()
class sensordata():
    device_id = 0
    aan_uit = 0
    lamp1 = 0
    lamp2 = 0
    lamp3 = 0
    lichtdetectie = 0
    autoset = 0
import datetime

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        optie = request.form['devices']
        #device = sensordata.query.filter_by(device_id=optie).first()
        query =   f'from(bucket: "TestOpstellingBaken")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "bakens" and r["id"] == "{optie}")\
            |> last()'

        result=read_api.query(org=org,query=query)
        data = sensordata()
        data.device_id = result[0].records[0].values.get("id")
        for i in range(len(result)):
            if result[i].records[0].get_field() == "aan_uit":
                data.aan_uit = result[i].records[0].get_value()
            elif result[i].records[0].get_field() == "lamp1":
                data.lamp1 = result[i].records[0].get_value()
            elif result[i].records[0].get_field() == "lamp2":
                data.lamp2 = result[i].records[0].get_value()
            elif result[i].records[0].get_field() == "lamp3":
                data.lamp3 = result[i].records[0].get_value()
            elif result[i].records[0].get_field() == "lichtdetectie":
                data.lichtdetectie = result[i].records[0].get_value()
            elif result[i].records[0].get_field() == "autoset":
                data.autoset = result[i].records[0].get_value()
        #ids = db.session.execute(db.select(sensordata).order_by(sensordata.device_id)).scalars()
        query =   'from(bucket: "TestOpstellingBaken")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "bakens")\
            |> filter(fn: (r) => r["_field"] == "autoset" )\
            |> last()'

        result=read_api.query(org=org,query=query)
        idlist=[]
        for i in range(0, len(result)):
            for record in result[i].records:
                idlist.append(record.values.get("id"))

        print(data.device_id)
        return render_template("base.html", device=data,ids=idlist)

    #ids = db.session.execute(db.select(sensordata).order_by(sensordata.device_id)).scalars()
    query =   'from(bucket: "TestOpstellingBaken")\
    |> range(start: 0)\
    |> filter(fn: (r) => r["_measurement"] == "bakens")\
    |> filter(fn: (r) => r["_field"] == "autoset" )\
    |> last()'

    result=read_api.query(org=org,query=query)
    idlist=[]
    for i in range(0, len(result)):
        for record in result[i].records:
            idlist.append(record.values.get("id"))
    return render_template("base.html",ids=idlist)


@app.route("/light/<device_id>", methods=["POST"])
def light(device_id):
    #device = sensordata.query.filter_by(device_id=device_id).first()
    #ids = db.session.execute(db.select(sensordata).order_by(sensordata.device_id)).scalars()
    query =   'from(bucket: "TestOpstellingBaken")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "bakens")\
            |> filter(fn: (r) => r["_field"] == "autoset" )\
            |> last()'

    result=read_api.query(org=org,query=query)
    idlist=[]
    for i in range(0, len(result)):
        for record in result[i].records:
            idlist.append(record.values.get("id"))

    value = request.form.get("submit")
    print(value)
    if value == "aan" or value == "uit":
            #device.autoset = 0
            #db.session.commit()
            data = influxdb_client.Point("bakens").tag("id",device_id).field("autoset",0)
            write_api.write(bucket=bucket,org=org,record=data)
            if value == "aan":
                print("lamp aan")
                create_downlink("LA1",device_id)
            if value == "uit":
                print("lamp uit")
                create_downlink("LA0",device_id)


    if value == "auto":
        print("set auto")
        #device.autoset = 1
        data = influxdb_client.Point("bakens").tag("id",device_id).field("autoset",1)
        write_api.write(bucket=bucket,org=org,record=data)
        #db.session.commit()
    query =   f'from(bucket: "TestOpstellingBaken")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "bakens" and r["id"] == "{device_id}")\
            |> last()'

    result=read_api.query(org=org,query=query)
    data = sensordata()
    data.device_id = result[0].records[0].values.get("id")
    for i in range(len(result)):
        if result[i].records[0].get_field() == "aan_uit":
            data.aan_uit = result[i].records[0].get_value()
        elif result[i].records[0].get_field() == "lamp1":
            data.lamp1 = result[i].records[0].get_value()
        elif result[i].records[0].get_field() == "lamp2":
            data.lamp2 = result[i].records[0].get_value()
        elif result[i].records[0].get_field() == "lamp3":
            data.lamp3 = result[i].records[0].get_value()
        elif result[i].records[0].get_field() == "lichtdetectie":
            data.lichtdetectie = result[i].records[0].get_value()
        elif result[i].records[0].get_field() == "autoset":
            data.autoset = result[i].records[0].get_value()

    return render_template("base.html",ids=idlist, device=data)


@app.route("/lights",methods={"POST"})
def alllights():
    #devices = db.session.execute(db.select(sensordata).order_by(sensordata.device_id)).scalars()
    query =   'from(bucket: "TestOpstellingBaken")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "bakens")\
            |> filter(fn: (r) => r["_field"] == "autoset" )\
            |> last()'

    result=read_api.query(org=org,query=query)
    idlist=[]
    for i in range(0, len(result)):
        for record in result[i].records:
            idlist.append(record.values.get("id"))
    value = request.form.get("submit")
    
    if value == "aan" or value == "uit":
        for device in idlist:
            #device.autoset = 0
            data = influxdb_client.Point("bakens").tag("id",device).field("autoset",0)
            write_api.write(bucket=bucket,org=org,record=data)
        #db.session.commit()

        if value == "aan":
            print("lampen aan")
            create_downlink_all("LA1")
        if value == "uit":
            print("lampen uit")
            create_downlink_all("LA0")
            
    if value == "auto":
        for device in idlist:
            #device.autoset = 1
            data = influxdb_client.Point("bakens").tag("id",device).field("autoset",1)
            write_api.write(bucket=bucket,org=org,record=data)
        #db.session.commit()
        print("lampen auto")


    return redirect(url_for("index"))