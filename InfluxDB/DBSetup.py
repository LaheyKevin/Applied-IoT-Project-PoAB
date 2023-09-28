##IS ENKEL OP DB TE INITEN
import datetime
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

##########INSERT
# data = influxdb_client.Point("bakens").tag("id","euid-125").field("aan_uit",0).field("lamp1",0).field("lamp2",0).field("lamp3",0).field("lichtdetectie",10).field("autoset",0)
# write_api.write(bucket=bucket,org=org,record=data)

##########READ
# query =   'from(bucket:"TestOpstellingBaken")\
# |> range(start: -30m)\
# |> filter(fn: (r) => r._measurement == "bakens")'
# #|> filter(fn: (r) => r.id == "euid-123")'
# #|> filter(fn: (r) => r._field == "aan_uit")'
# result=read_api.query(org=org,query=query)
# results = []
# for table in result:
#     for record in table.records:
#         print(record.values)
#         results.append((record.get_field(), record.get_value()))
# print(results)

##########DELETE
# delete_api = DBclient.delete_api()
# start="2021-09-22T18:37:08Z"
# stop="2024-09-22T19:37:08Z"
# delete_api.delete(start=start, stop=stop, predicate='_measurement="bakens"', org=org, bucket=bucket)
# #"_measurement=\"bakens\" AND id=\"euid-123\""

##########UPDATE
#To update you need same Point and same tag to update the fields
# data = influxdb_client.Point("bakens").tag("id","euid-124").field("lichtdetectie",1081)#.time(datetime.datetime(2023, 9, 22, 17, 59, 1, 909436))
# write_api.write(bucket=bucket,org=org,record=data)