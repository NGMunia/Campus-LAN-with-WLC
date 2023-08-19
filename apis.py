from Network.Devices import Routers,Switches
from netmiko import ConnectHandler
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import ntc_templates
from jinja2 import FileSystemLoader, Environment


app = FastAPI()

'''
Configuring VLANs on Switches
'''
class vlanclass(BaseModel):
    vlan_ID : int
    vlan_name : str
    access_ports : str
    Access_switch : bool
@app.post('/Devices/Switches/{Switch_name}/Configure/VLAN', status_code=status.HTTP_201_CREATED)
def vlanconf(post:vlanclass, Switch_name: str):
    device = Switches[Switch_name]
    conn = ConnectHandler(**device)
    conn.enable()

    if post.vlan_ID == 1 or post.vlan_ID >=1002:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid VLAN number')
    elif post.Access_switch == False:
        commands = ['vlan '+str(post.vlan_ID),'name '+post.vlan_name,'interface vlan '+str(post.vlan_ID),
                    'ip address 10.1.'+str(post.vlan_ID)+'.1 255.255.255.0','no shut']
    else:
        commands = ['vlan '+str(post.vlan_ID),'name '+post.vlan_name,'interface '+post.access_ports,
                    'switchport access vlan '+str(post.vlan_ID)]
    
    result = conn.send_config_set(commands)
    conn.disconnect()
    return result.splitlines()
  

'''
Configuring DHCP on Core/Distribution Switch
'''
class dhcpclass(BaseModel):
    DHCP_name : str
    vlan_ID : int
@app.post('/Devices/Switches/{Switch_name}/Configure/DHCP',status_code=status.HTTP_201_CREATED)
def dhcpconf(post:dhcpclass, Switch_name: str):
    device = Switches[Switch_name]
    conn = ConnectHandler(**device)
    conn.enable()

    commands = ['ip dhcp excluded-address 10.1.'+str(post.vlan_ID)+'.1 10.1.'+str(post.vlan_ID)+'.10',
                'ip dhcp pool VLAN_'+str(post.vlan_ID)+'_POOL',
                'network 10.1.'+str(post.vlan_ID)+'.0 255.255.255.0',
                'default-router 10.1.'+str(post.vlan_ID)+'.1',
                'dns-server 8.8.8.8']
    result = conn.send_config_set(commands)
    return result.splitlines()


'''
Configuring ACLs restricting Remote access to Management-VLAN on switches
'''
@app.post('/Devices/Switches/{Switch_name}/Configure/VTY_ACL',status_code=status.HTTP_201_CREATED)
def vtyacl(Switch_name : str):
    Device = Switches[Switch_name]
    conn = ConnectHandler(**Device)
    conn.enable()

    commands = ['ip access-list extended VTY_ACL',
                'permit tcp 10.1.255.0 0.0.0.255 any eq 22',
                'deny tcp any any log',
                'line vty 0 4',
                'access-class VTY_ACL in']
    result = conn.send_config_set(commands)
    return result.splitlines()
    
    
'''
Configuring ACLs restricting Remote access to Management-VLAN on Routers
'''
@app.post('/Devices/Routers/{Router_name}/Configure/VTY_ACL',status_code=status.HTTP_201_CREATED)
def vtyacl(Router_name : str):
    Device = Routers[Router_name]
    conn = ConnectHandler(**Device)
    conn.enable()

    commands = ['ip access-list extended VTY_ACL',
                'permit tcp 10.1.255.0 0.0.0.255 any eq 22',
                'deny tcp any any log',
                'line vty 0 4',
                'access-class VTY_ACL in']
    result = conn.send_config_set(commands)
    return result.splitlines()


'''
Configuring NTP on Routers
'''
class ntpclass(BaseModel):
    ntp_server : str
    template_path : str
@app.post('/Devices/Routers/{Router_name}/Configure/NTP', status_code=status.HTTP_201_CREATED)
def ntpconf(Router_name:str, post:ntpclass):
    device = Routers[Router_name]
    conn = ConnectHandler(**device)
    conn.enable()

    env = Environment(loader=FileSystemLoader(post.template_path))
    template = env.get_template('ntp.j2')
    variables= {'ntp_server': post.ntp_server}

    commands = template.render(variables)
    result   = conn.send_config_set(commands.splitlines())
    return result.splitlines()


'''
API GET VLAN information
'''
@app.get('/Devices/Switches/{Switch_name}/get/VLANs')
def getvlans(Switch_name: str):
    device = Switches[Switch_name]
    conn = ConnectHandler(**device)
    conn.enable()

    result = conn.send_command('show vlan brief',use_textfsm=True)
    return f'Switch {Switch_name}',result
