
import requests
import os
import json
import os

root_path ='/data/consul/data/services'
all_service = {}
del_service =[]
def getService(filepath):

  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)
    if os.path.isdir(fi_d):
        getService(fi_d)
    else:
        filepath, shotname, extension = get_filePath_fileName_fileExt(os.path.join(filepath,fi_d))
        if shotname!='.DS_Store':

            try:
                with open(os.path.join(filepath,fi_d), 'r') as load_f:
                    load_dict = json.load(load_f)
                    all_service[shotname]=load_dict
            except IOError:
                print(shotname+'  error')


def get_filePath_fileName_fileExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return filepath,shotname,extension

if __name__ == "__main__":
    getService(root_path)
    consul_critical_url = "http://10.23.27.87/v1/health/state/critical"
    critical_result = requests.get(consul_critical_url)
    if critical_result.status_code==200:
        critical_service_list =  json.loads(critical_result.text)
        for node_service in critical_service_list:
            node_service_id = node_service["ServiceID"]

            for key in all_service:
                local_service_id =all_service[key]["Service"]["ID"]
                if(node_service_id == local_service_id):
                    del_service.append(key)
    for del_service_name in del_service:
        if os.path.exists(root_path+'/'+del_service_name):
            os.remove(root_path+'/'+del_service_name)
            print('del='+root_path+'/'+del_service_name)









