import requests 
import re                                                                
import os

HOST = "http://pnrr-ai.ase.ro"
TIMEOUT = 3
WRITE_FILE = "/etc/jupyterhub/custom_templates/active_users"

def get_active_users():                     
    try:                                                                                                                
        headers = {                                                                                                         
           "Authorization": f"Bearer {os.environ['PROMETHEUS_TOKEN']}",                                
        }                                                                                                                                                                                                        
        proxy_address = f"{HOST}/hub/metrics"                                                               
        metrics = requests.get(proxy_address, headers=headers, verify=False, timeout=TIMEOUT)                                                                                        
        active_users_match = re.match(r"jupyterhub_running_servers (\d+)\.0.*", metrics.text, flags=re.MULTILINE)
        if active_users_match is not None:
            active_users = active_users_match.group(1)
        else:
            active_users = "[regex error]"                         
    except Exception as e:
        active_users = f"{e}"                                                         
    print(f"Active users: {active_users}")
    return active_users 

active_users = get_active_users()

with open(WRITE_FILE, "w") as f:
    if active_users != "":
        f.write(active_users)
    else:
        f.write("")

