import iperf3, json, time, sys, getopt
from influxdb import InfluxDBClient

INFLUX_DB_IP = '192.168.1.10'


def net_test(host, ssid, ap_info):
    clientDB = InfluxDBClient(INFLUX_DB_IP, 8086, 'network_logger', 'gowifi!', 'network_benchmark')



    while True:
        client = iperf3.Client()
        client.duration = 5
        client.server_hostname = host
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
        influx_data["tags"] = {"wifi_ssid" : ssid, "status" : status, "access_point_info" : ap_info}
        influx_data["fields"] = {"sent": sent}

        # influx_data = json.dumps(influx_data)
        print (influx_data)

        clientDB.write_points([influx_data])
        time.sleep(10)


def main(argv):
    host_ip = '192.168.1.10'
    ssid = 'unknown'
    ap_info = 'unknown'
    try:
        opts, args = getopt.getopt(argv,"hs:o:a:",["ssid=","output_host=","ap_info="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('net_test.py -o <host_name> -s <SSID> -a <access_point_info>')
            sys.exit()
        elif opt in ("-s", "--ssid"):
            ssid = arg
        elif opt in ("-o", "--output_host"):
            host_ip = arg
        elif opt in ("-a", "--ap_info"):
            ap_info = arg
            
    
    net_test(host_ip, ssid, ap_info)

if __name__ == "__main__":
   main(sys.argv[1:])