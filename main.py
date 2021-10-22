import wifi
import usocket
import esp32

print('Executing code')
pd_host = '192.168.1.114'
pd_port = 15000
wifi.wifi_connect()
pd = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
pd.connect((pd_host, pd_port))
print('Connected to {}:{}'.format(pd_host, pd_port))
while True:
    pot_value = pot.read()
    pd.send(pot_value.to_bytes(8,"big"))
    utime.sleep_ms(200)
