from machine import Pin, PWM, SoftI2C, time_pulse_us
from mpu6050 import MPU6050
from utime import sleep
import math

# Wokwi: los datos se quedan en listas (no hay CSV en el simulador)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  # SDA=21, SCL=22
print("I2C scan:", i2c.scan())
mpu = MPU6050(i2c)
trig = Pin(4, Pin.OUT)          # ultrasónico TRIG
echo = Pin(5, Pin.IN)           # ultrasónico ECHO
led = PWM(Pin(26))
buzzer = PWM(Pin(25))
servo = PWM(Pin(18), freq=50)   # señal del servo
led.duty(0)
buzzer.duty(0)
modos = ["IZQUIERDA", "DERECHA"]
LIMITE_CM = 15
ANG_IZQ = 45
ANG_DER = 135
ANG_STOP = 90
ultimo = ""
ok = 0
paradas = 0

def leer():
    ax, ay, az, gx, gy, gz = mpu.leer()
    vib = abs(math.sqrt(ax**2 + ay**2 + az**2) - 1)  # sube si agitas (rotation)
    return (ax, ay), vib          # ax y ay SIN abs: así se distingue izq de der

def distancia_cm():
    trig.off()
    sleep(0.00001)
    trig.on()
    sleep(0.00001)
    trig.off()
    t = time_pulse_us(echo, 1, 30000)  # Wokwi: mejor que un while
    if t < 0:
        return 400.0
    cm = (t * 0.0343) / 2
    if cm < 2 or cm > 400:
        return 400.0
    return cm

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def kmeans(datos, k=2):
    n = len(datos)
    centros = [datos[0], datos[n // 2]]
    for _ in range(8):
        grupos = [[] for _ in range(k)]
        for p in datos:
            d = [dist(p, c) for c in centros]
            grupos[d.index(min(d))].append(p)
        for i in range(k):
            if grupos[i]:
                mx = sum(p[0] for p in grupos[i]) / len(grupos[i])
                my = sum(p[1] for p in grupos[i]) / len(grupos[i])
                centros[i] = (mx, my)
    intramax = max(min(dist(p, c) for c in centros) for p in datos)
    entre = dist(centros[0], centros[1])
    umbral = max(entre * 0.45, intramax * 1.2, 0.25)
    return centros, umbral

def angulo(g):
    us = 500 + (g / 180.0) * 2000
    servo.duty_u16(int(us / 20000.0 * 65535))

def parar():
    global ultimo
    led.duty(0)
    buzzer.freq(2000)
    buzzer.duty(512)
    if ultimo == "STOP":
        return
    ultimo = "STOP"
    angulo(ANG_STOP)

def producir(lado):
    global ultimo
    buzzer.duty(0)
    if lado == "IZQ":
        led.duty(400)
        g = ANG_IZQ
    else:
        led.duty(900)
        g = ANG_DER
    if ultimo == lado:
        return
    ultimo = lado
    angulo(g)

angulo(ANG_STOP)

# 1) Recolectar en memoria (Wokwi no usa CSV)
print("Wokwi: clic en el MPU6050 para mover accelX / accelY")
grupos = {"IZQUIERDA": [], "DERECHA": []}
vibs = []
for modo in modos:
    if modo == "IZQUIERDA":
        print("Pon accelY = -1 (y accelX = 0). Mantén 5 muestras")
    else:
        print("Pon accelY = 1 (y accelX = 0). Mantén 5 muestras")
    sleep(8)                      # tiempo para mover los sliders
    for i in range(5):
        p, vib = leer()
        grupos[modo].append(p)
        vibs.append(vib)
        print(i + 1, "ax=", round(p[0], 2), "ay=", round(p[1], 2))
        sleep(0.3)

# 2) K-means K=2 con las listas (sin archivo)
datos = grupos["IZQUIERDA"] + grupos["DERECHA"]
centros, umbral = kmeans(datos)
umbral_vib = max(max(vibs) * 3.0, 0.12)
mean_izq = (
    sum(p[0] for p in grupos["IZQUIERDA"]) / 5,
    sum(p[1] for p in grupos["IZQUIERDA"]) / 5,
)
mean_der = (
    sum(p[0] for p in grupos["DERECHA"]) / 5,
    sum(p[1] for p in grupos["DERECHA"]) / 5,
)
etiqueta = []
for c in centros:
    if dist(c, mean_izq) < dist(c, mean_der):
        etiqueta.append("IZQ")
    else:
        etiqueta.append("DER")
if etiqueta[0] == etiqueta[1]:
    etiqueta = ["IZQ", "DER"]
print("umbral dist=", round(umbral, 3), " umbral vib=", round(umbral_vib, 3))
print("centros:", etiqueta[0], centros[0], etiqueta[1], centros[1])
print("En vivo: IZQ=45 DER=135. Anomalia: accelZ=-1 o sube rotation. Obstaculo: slider < 15 cm")

# 3) En vivo
while True:
    p, vib = leer()
    cm = distancia_cm()
    d0 = dist(p, centros[0])
    d1 = dist(p, centros[1])
    if d0 <= d1:
        idx, menor = 0, d0
    else:
        idx, menor = 1, d1
    if 2 < cm < LIMITE_CM:
        parar()
        paradas += 1
        print("STOP ultrasónico", round(cm, 1), "cm")
    elif menor > umbral or vib > umbral_vib:
        parar()
        paradas += 1
        print("ANOMALIA dist=", round(menor, 3), "vib=", round(vib, 3), "STOP")
    else:
        producir(etiqueta[idx])
        ok += 1
        print(etiqueta[idx], "dist=", round(menor, 3), "ax=", round(p[0], 2), "ay=", round(p[1], 2))
    sleep(0.3)
