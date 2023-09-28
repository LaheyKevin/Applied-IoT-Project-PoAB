
from app import app
import paho.mqtt.client as mqtt
import base64
import json
import certifi

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

APPID  = "portofantwerp-2023@ttn"
PSW    = 'NNSXS.2F7ZVD6AVRIBI4O7WOYSTPKDWMPG66NL2L6CARI.K3EHQPN5FLRTSTBF6NBJ4LPKF7V4Z2QVZQ5LMTBMGGPLMUN44EIA'

#conn = sqlite3.connect("LoRa.db", check_same_thread=False)

client = mqtt.Client()

#subscriben op de mqtt topic van alle devices
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = "#"
    #topic = "v3/{}/devices/{}/up".format(APPID,"eui-a8610a30373d9301") 
    client.subscribe(topic,0)

#ontvangen berichten van de devices verwerken
def on_message(client, userdata, msg):
    x = json.loads(msg.payload.decode('utf-8'))

    device_id = x["end_device_ids"]["device_id"]

    if "uplink_message" in x and device_id == "eui-a8610a30373d9301":
        print(x)
        print(f"device id is {device_id}")
        payoload = x["uplink_message"]["decoded_payload"]["payload"]
        print(f"de payload is {payoload}")

        payoload_data=list(payoload.split(":"))

        payoload_data = [int(i) for i in payoload_data]

        print(payoload_data)

        query=f'from(bucket: "TestOpstellingBaken")\
        |> range(start: 0)\
        |> filter(fn: (r) => r["_measurement"] == "bakens")\
        |> filter(fn: (r) => r["id"] == "{device_id}")'

        result=read_api.query(org=org,query=query)
        if result:  
            data = influxdb_client.Point("bakens").tag("id",device_id).field("aan_uit",payoload_data[0]).field("lamp1",payoload_data[1]).field("lamp2",payoload_data[2]).field("lamp3",payoload_data[3]).field("lichtdetectie",payoload_data[4])
        else:   #Nieuwe baken + dataset
            data = influxdb_client.Point("bakens").tag("id",device_id).field("aan_uit",payoload_data[0]).field("lamp1",payoload_data[1]).field("lamp2",payoload_data[2]).field("lamp3",payoload_data[3]).field("lichtdetectie",payoload_data[4]).field("autoset",0)
        write_api.write(bucket=bucket,org=org,record=data)

        #het gemidelde berkennen en nodige aansturing vanuit toepassing doen
        # conn.row_factory = lambda cursor, row: row[0]
        # c = conn.cursor()
        # gemidelde = c.execute(f"SELECT AVG(lichtdetectie) FROM sensordata where autoset = 1")
        # avg = int(gemidelde.fetchall()[0])

        query =   'from(bucket: "TestOpstellingBaken")\
        |> range(start: 0)\
        |> filter(fn: (r) => r["_measurement"] == "bakens")\
        |> filter(fn: (r) => r["_field"] == "autoset" or r["_field"] == "lichtdetectie")\
        |> last()'

        result=read_api.query(org=org,query=query)
        avg = [0,0] #Result + count
        for i in range(0, len(result), 2):
            for record in result[i].records:
                if record.get_value() == 1:
                    avg[0] += result[i+1].records[0].get_value()
                    avg[1] += 1

        if avg[0] != 0:
            avg[0] = int(avg[0]/avg[1])
        else:
            avg[0] == None

        if avg[0] is not None:
            print(f"Het licht gemidelde: {avg[0]}, aantal autoset: {avg[1]}")
            
            if avg[0] < 400:
                print("lamp aan door gemidelde")
                create_downlink_all("LA1")
            
            if avg[0] > 600:
                print("lampen uit door gemidelde")
                create_downlink_all("LA0")

#verbinding afsluiten
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

#sturen naar 1 bepaalde device
def create_downlink(data,device_id):
    data = data.encode("ascii")
    data = base64.b64encode(data)
    data = data.decode("ascii")
    print(data)
    payload = {
    "downlinks": [
            {
                "f_port": 1,                    
                "frm_payload": str(data),  
               "priority": "NORMAL"          
            }
        ]
    }
    
    payload_json = json.dumps(payload)
    topic = "v3/{}/devices/{}/down/push".format(APPID, device_id)  
    client.publish(topic,payload_json)


#sturen naar alle devices die op auto staan
def create_downlink_all(data):

    data = data.encode("ascii")
    data = base64.b64encode(data)
    data = data.decode("ascii")
    print(f"data naar alle devices: {data}")
    #conn.row_factory = lambda cursor, row: row[0]
    #c = conn.cursor()
    #idlist = c.execute(f"SELECT device_id FROM sensordata where autoset = 1").fetchall()

    query =   'from(bucket: "TestOpstellingBaken")\
    |> range(start: 0)\
    |> filter(fn: (r) => r["_measurement"] == "bakens")\
    |> filter(fn: (r) => r["_field"] == "autoset" and r["_value"] == 1)\
    |> last()'

    result=read_api.query(org=org,query=query)
    idlist=[]
    for i in range(0, len(result)):
        for record in result[i].records:
            idlist.append(record.values.get("id"))

    print(idlist)
    if idlist != []:
        for id in idlist:
            # autoset = c.execute(f"SELECT autoset FROM sensordata").fetchall()
            # print(autoset)
        
            payload = {
                "downlinks": [
                    {
                        "f_port": 1,                    
                        "frm_payload": str(data),  
                    "priority": "NORMAL"          
                    }
                ]
            }
            payload_json = json.dumps(payload)
            topic = "v3/{}/devices/{}/down/push".format(APPID, id)  
            client.publish(topic,payload_json)
    else:
        print("Geen devices met autoset 1")


#gepubliseerd bricht status bekijken
def on_publish(client, userdata, mid):
    print("Message published with MID: " + str(mid))
    

cafile = certifi.where()


#de callback functies zetten
client.on_connect = on_connect
client.on_message = on_message
client.on_publish= on_publish

#verbinding maken met mqtt broker
client.enable_logger()
client.tls_set(ca_certs=certifi.where())
client.username_pw_set(APPID, PSW)
client.connect("eu1.cloud.thethings.network", 8883,60)

client.loop_start() 
