from Network.Devices import Routers, Switches
from netmiko import ConnectHandler
from rich import print as rp
from csv import writer
import ntc_templates

'''
Getting Device inventory
'''
filepath = input('Filepath: ')
with open(f'{filepath}/inventory.csv','w') as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP-Address','Sofware-Version','Serial-No'])

    for routers in Routers.values():
        conn = ConnectHandler(**routers)
        conn.enable()
        output = conn.send_command('show version',use_textfsm=True)[0]

        #Variables
        hostname =  output['hostname']
        ip_addr  = routers['ip']
        version  =  output['version']
        serial   =  output['serial']

        write_data.writerow([hostname,ip_addr,version,serial])
        rp(f'Finished getting the Inventory for Router {hostname}')

    for switches in Switches.values():
        conn = ConnectHandler(**switches)
        conn.enable()
        output = conn.send_command('show version',use_textfsm=True)[0]

        #Variables
        hostname =   output['hostname']
        ip_addr  = switches['ip']
        version  =   output['version']
        serial   =   output['serial']

        write_data.writerow([hostname,ip_addr,version,serial])
        rp(f'Finished getting the Inventory for Switch {hostname}')

        

    
