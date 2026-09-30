from machine import Pin, PWM, ADC, time_pulse_us
from utime import sleep, sleep_us

# Importar librerías y configurar pines
ldr = ADC(Pin(35))            # luz en la "cabeza" del radar
trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)
servo = PWM(Pin(23))
led = Pin(26, Pin.OUT)
ldr.atten(ADC.ATTN_11DB)
servo.freq(50)
led.off()
PASO = 10                     # grados entre lecturas (0, 10, ... 180)

# Definir funciones
def angulo(g):
    us = 500 + (g / 180.0) * 2000
    d = int(us / 20000.0 * 1023)
    if d < 26:
        d = 26
    if d > 128:
        d = 128
    servo.duty(d)

def distancia_cm():
    trig.off()
    sleep_us(2)
    trig.on()
    sleep_us(10)
    trig.off()
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return 400.0
    cm = (t * 0.0343) / 2
    if cm < 2 or cm > 400:
        return 400.0
    return cm

def luz_pct():
    return (ldr.read() / 4095.0) * 100.0

# 1) Ir a 0 grados y abrir el CSV
angulo(0)
sleep(1)
archivo = open("datos.csv", "w")
archivo.write("angulo,luz,cm\n")

# 2) Barrer: en cada angulo leer luz y distancia
g = 0
while g <= 180:
    angulo(g)
    led.on()
    sleep(0.4)
    luz = luz_pct()
    cm = distancia_cm()
    archivo.write("{:d},{:.1f},{:.1f}\n".format(g, luz, cm))
    print("ang=", g, "luz=", round(luz, 1), "cm=", round(cm, 1))
    g = g + PASO
archivo.close()
led.off()
angulo(90)

# 3) Listo: baja datos.csv y corre graficar.py en la PC
print("Barrido listo. Baja datos.csv y corre graficar.py")
