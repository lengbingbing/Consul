
import requests
import json
import os
import re
import consul


import time


consul_address= ""
port=8500
service_name=""
test = False
server_list = []
if test:
    server_list =["10.23.26.2","192.168.205.17","192.168.205.18"]
    consul_address = "10.23.27.87"
    service_name = "openapi-lan-cassandra"
    port =80
else:
    server_list =["10.168.99.54"]
    consul_address = "10.168.100.164"
    service_name = "openapi-lan-cassandra"
    port = 8500



def valid_ip(ip):
    if ("255" in ip) or ( ip == "127.0.0.1") or ( ip == "0.0.0.0" ):
        return False
    else:
        return True

def get_ip(valid_ip):
    ipss = ''.join(os.popen("ifconfig").readlines())
    match = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(match, ipss, flags=re.M)
    ip = filter(valid_ip, ips)
    return ''.join(ip)


if __name__ == "__main__":



    while True:
        all_service = {}
        find_service = []

        consul_critical_url = "http://"+consul_address+":"+str(port)+"/v1/health/state/critical"
        critical_result = requests.get(consul_critical_url)
        if critical_result.status_code==200:
            critical_service_list =  json.loads(critical_result.text)
            for node_service in critical_service_list:
                if node_service["ServiceName"]==service_name:
                    find_service.append(node_service)


        for service in find_service:

            current_ip = get_ip(valid_ip)
            if (len(find_service) == len(server_list)):
                    print("current_ip=" + current_ip)
                    client = consul.Consul(host=consul_address, port=port)
                    index = None
                    index, data = client.kv.get('uc/openapi/runing_nginx/'+current_ip, index=index)
                    if(data==None):
                        print("data not none" )
                        for server_ip in server_list:
                            print("server_ip=" + server_ip)
                            if server_ip==current_ip:
                                client.kv.put('uc/openapi/runing_nginx/' + current_ip, current_ip)
                                print("start emergency")
                                os.system("sh safety.sh")

                                break
                    else:
                        print("emergency runing")

            else:
                print("emergency not active,len(find_service)="+str(len(find_service))+"len(server_list="+str(len(server_list)))




        time.sleep(5)



