#removed os lib import
import subprocess

ips = {'site-name':'0.0.0.0', 'site-name': '0.0.0.0',
       'site-name': '0.0.0.0', 'site-name': '0.0.0.0',
       'site-name': '0.0.0.0', 'site-name': '0.0.0.0'}

def ping_stores():
    for name, value in ips.items():
        process = subprocess.call(['ping', '-n', '5', value])
        if process == 0:



            print ("ping to", name, "OK")
        elif process == 2:
            print ("no response from", name)
        else:
            print ("ping to", name, "failed!")
            
stores = ping_stores()
stores
