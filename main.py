import wifi
import usocket
import utime
from machine import Pin, ADC, PWM
import _thread

def serverThread():
    # Modificar Pin segun sus conexiones yo usé 12 como ejemplo
    pwm = PWM(Pin(12))
    ## Para modificar la freq (no es necesario para el L298N)
    ## Por defecto para ESP32 es 5kHz y para ESP8266 es 1kHz
    # pwm.freq(VALOR_FREQ)
    ## Para modificar el ciclo util entre 0 y 1023 (0 para 0%, 1023 para 100%)
    pwm.duty(600)
    addr = usocket.getaddrinfo('0.0.0.0', 5050)[0][-1]
    server = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    server.bind(addr)
    print('Servidor listo para recibir')
    while True:
        data, direccion = server.recvfrom(2)
        print('De: {}: recibi:{}'.format(direccion,data))
        # Para mover el motor con el L298 es convertir el valor que se recibe
        # en un valor para el ciclo util Ej:
        # pwm.duty(data)
        # **OJO, tambien deben decidir con pines normales la direccion del giro.

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
