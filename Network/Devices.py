from rich import print as rp
Routers =  {
           'Edge':   {
                       'device_type' : 'cisco_ios',
                       'ip' : '10.1.1.6',
                       'username' : 'Automation',
                       'password' : 'cisco123',
                       'secret' : 'cisco123'
                     },
          'firewall':{
                       'device_type' : 'cisco_ios',
                       'ip' : '10.1.1.5',
                       'username' : 'Automation',
                       'password' : 'cisco123',
                       'secret' : 'cisco123'        
                     }    
           }

Switches = {
             'CORE': {
                       'device_type' : 'cisco_ios',
                       'ip' : '10.1.255.1',
                       'username' : 'Automation',
                       'password' : 'cisco123',
                       'secret' : 'cisco123'
                     },
              'SW1': {
                        'device_type' : 'cisco_ios',
                        'ip' : '10.1.255.2',
                        'username' : 'Automation',
                        'password' : 'cisco123',
                        'secret' : 'cisco123'
                     },
              'SW2': {
                        'device_type' : 'cisco_ios',
                        'ip' : '10.1.255.3',
                        'username' : 'Automation',
                        'password' : 'cisco123',
                        'secret' : 'cisco123'
                     }, 
              'SW3': {
                        'device_type' : 'cisco_ios',
                        'ip' : '10.1.255.4',
                        'username' : 'Automation',
                        'password' : 'cisco123',
                        'secret' : 'cisco123'
                     }     
           }