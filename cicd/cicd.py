import os
import shutil

# Check installation of rsyslog
if os.system('systemctl status rsyslog') > 0:
    print('uninstalled')
    '''
    yum install rsyslog
    systemctl enable rsyslog
    systemctl start rsyslog
    '''
else:
    # copy new configuration files
    shutil.copy(./)
    print('ok')
