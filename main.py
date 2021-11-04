import wifi
import usocket
import utime
from machine import Pin, ADC
import _thread

def serverThread():
    addr = usocket.getaddrinfo('0.0.0.0', 5050)[0][-1]
    server = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    server.bind(addr)
    print('Servidor listo para recibir')
    while True:
        data, direccion = server.recvfrom(2)
        print('De: {}: recibi:{}'.format(direccion,data))


ldr = ADC(Pin(32))
ldr2 = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)       #Full range: 3.3v
#ldr2.atten(ADC.ATTN_11DB)

pd_host = '192.168.1.115'
pd_port = 4444
wifi.wifi_connect()
print('Executing code')
pd = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
pd.connect((pd_host, pd_port))
print('Connected to {}:{}'.format(pd_host, pd_port))
_thread.start_new_thread(serverThread, ())
while True:
    ldr_value = ldr.read()
    ldr2_value = ldr2.read()
    pd.send(ldr_value.to_bytes(2,"big") + (ldr2_value.to_bytes(2,"big")))
    # print(ldr_value)
    utime.sleep_ms(20)
