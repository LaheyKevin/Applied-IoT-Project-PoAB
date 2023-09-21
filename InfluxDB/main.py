#https://www.influxdata.com/blog/getting-started-python-influxdb/
#https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

token = "jw-O_3q5SVuqGDN2jjWtvtRP3q8f80DXX0mQyqozDbFVA203KyWLlwxelp8SCY1lzEUNRwJc_e8lZzkFg8o93Q=="
org = "AP"
url = "http://127.0.0.1:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# bucket="HavenTest"
# write_api = write_client.write_api(write_options=SYNCHRONOUS)
# for value in range(5):
#   point = (
#     Point("measurement1")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#   )
#   write_api.write(bucket=bucket, org="AP", record=point)
#   time.sleep(1) # separate points by 1 second


query_api = write_client.query_api()
query = """from(bucket: "HavenTest")
 |> range(start: -800m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="AP")
for table in tables:
  for record in table.records:
    with open("test.json","w") as file:
      file.write(str(record))
    print(record.get_value())
    print("\n")


# query_api = write_client.query_api()
# query = """from(bucket: "HavenTest")
#   |> range(start: -10m)
#   |> filter(fn: (r) => r._measurement == "measurement1")
#   |> mean()"""
# tables = query_api.query(query, org="AP")
# for table in tables:
#     for record in table.records:
#         print(record)
#         print("\n")
