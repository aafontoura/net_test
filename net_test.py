import iperf3, json, time
from influxdb import InfluxDBClient


clientDB = InfluxDBClient('192.168.1.10', 8086, 'network_logger', 'gowifi!', 'network_benchmark')



while True:
    client = iperf3.Client()
    client.duration = 5
    client.server_hostname = '192.168.1.10'
    client.port = 5201
    # result = client.run()
    try:
        result = client.run()
    except Exception as ex:
        print (ex)

        time.sleep(10)
        continue
    try:
        sent = result.sent_Mbps 
        status = "Online"
    except:
        sent = 0.0
        status = "Offline"
    del(client)

    influx_data = {}
    influx_data["measurement"] = "local_connection_speed"
    influx_data["tags"] = {"wifi_ssid" : "internacional", "status" : status}
    influx_data["fields"] = {"sent": sent}

    # influx_data = json.dumps(influx_data)
    print (influx_data)

    clientDB.write_points([influx_data])
    time.sleep(10)
