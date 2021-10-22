import wifi
import usocket

print('Executing code')
pd_host = '192.168.1.114'
pd_port = 15000
wifi.wifi_connect()
pd = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
pd.connect((pd_host, pd_port))
