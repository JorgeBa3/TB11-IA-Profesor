from machine import Pin, PWM, SoftI2C
from mpu6050 import MPU6050
from utime import sleep, ticks_us, ticks_diff
import math

# Importar librerías y configurar pines
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  # SDA=21, SCL=22
print("I2C scan:", i2c.scan())
mpu = MPU6050(i2c)
trig = Pin(4, Pin.OUT)          # ultrasónico TRIG
echo = Pin(5, Pin.IN)           # ultrasónico ECHO
led = PWM(Pin(26))
buzzer = PWM(Pin(25))
servo = PWM(Pin(18), freq=50)   # señal PWM; el 5V alimenta el servo
led.duty(0)
buzzer.duty(0)
modos = ["IZQUIERDA", "DERECHA"]  # las dos poses que vas a guardar
LIMITE_CM = 15                    # parar si hay un obstáculo más cerca
ANG_IZQ = 45                      # brazo clasifica a la izquierda
ANG_DER = 135                     # brazo clasifica a la derecha
ANG_STOP = 90                     # posición segura (centro)
ultimo = ""                       # último modo, para no mover el servo de más
ok = 0
paradas = 0

# Definir funciones
def leer():
    ax, ay, az, gx, gy, gz = mpu.leer()
    vib = abs(math.sqrt(ax**2 + ay**2 + az**2) - 1)  # 0 en reposo; sube si agitas
    return (ax, ay), vib          # ax y ay SIN abs: así se distingue izq de der

def distancia_cm():
    trig.off()
    sleep(0.00001)
    trig.on()
    sleep(0.00001)
    trig.off()                    # pulso de 10 us para disparar el HC-SR04
    espera = ticks_us()
    t_ini = espera
    while echo.value() == 0:
        if ticks_diff(ticks_us(), espera) > 30000:
            return 400.0          # no llegó el eco (timeout)
        t_ini = ticks_us()
    espera = ticks_us()
    t_fin = t_ini
    while echo.value() == 1:
        if ticks_diff(ticks_us(), espera) > 30000:
            return 400.0
        t_fin = ticks_us()
    cm = (ticks_diff(t_fin, t_ini) * 0.0343) / 2  # ida y vuelta del sonido
    if cm < 2 or cm > 400:
        return 400.0
    return cm

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)  # distancia euclidiana

def kmeans(datos, k=2):
    n = len(datos)
    centros = [datos[0], datos[n // 2]]  # un centro por pose (izq y der)
    for _ in range(8):
        grupos = [[] for _ in range(k)]
        for p in datos:
            d = [dist(p, c) for c in centros]
            grupos[d.index(min(d))].append(p)  # cada punto al centro más cercano
        for i in range(k):
            if grupos[i]:
                mx = sum(p[0] for p in grupos[i]) / len(grupos[i])
                my = sum(p[1] for p in grupos[i]) / len(grupos[i])
                centros[i] = (mx, my)          # el centro se mueve al promedio
    intramax = max(min(dist(p, c) for c in centros) for p in datos)
    entre = dist(centros[0], centros[1])       # qué tan separados quedaron
    umbral = max(entre * 0.45, intramax * 1.2, 0.25)  # más lejos = anomalía
    return centros, umbral

def angulo(g):
    us = 500 + (g / 180.0) * 2000  # 0°=0.5 ms, 180°=2.5 ms (SG90)
    servo.duty_u16(int(us / 20000.0 * 65535))

def parar():
    global ultimo
    led.duty(0)
    buzzer.freq(2000)
    buzzer.duty(512)              # alerta de parada
    if ultimo == "STOP":
        return
    ultimo = "STOP"
    angulo(ANG_STOP)              # brazo al centro: no clasifica

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
    angulo(g)                     # IZQ y DER sí se ven distintos en el brazo

angulo(ANG_STOP)                  # empieza en el centro

# 1) Recolectar CSV: IZQUIERDA y DERECHA (ax, ay, sin abs)
archivo = open("datos.csv", "w")
archivo.write("ax,ay\n")
grupos = {"IZQUIERDA": [], "DERECHA": []}
vibs = []
for modo in modos:
    print("Inclina el MPU6050 a la", modo, "y mantenlo")
    sleep(3)                      # tiempo para colocar el sensor
    for i in range(5):
        p, vib = leer()
        grupos[modo].append(p)
        vibs.append(vib)
        archivo.write("{:.3f},{:.3f}\n".format(p[0], p[1]))
        print(i + 1, "ax=", round(p[0], 2), "ay=", round(p[1], 2))
        sleep(0.3)
archivo.close()

# 2) K-means K=2 y etiquetas IZQ/DER segun lo que guardaste
datos = grupos["IZQUIERDA"] + grupos["DERECHA"]
centros, umbral = kmeans(datos)
umbral_vib = max(max(vibs) * 3.0, 0.12)  # agitar más que en el entrenamiento
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
        etiqueta.append("IZQ")    # este centro es el que guardaste a la izquierda
    else:
        etiqueta.append("DER")
if etiqueta[0] == etiqueta[1]:
    etiqueta = ["IZQ", "DER"]     # por si los dos centros cayeron del mismo lado
print("umbral dist=", round(umbral, 3), " umbral vib=", round(umbral_vib, 3))
print("centros:", etiqueta[0], centros[0], etiqueta[1], centros[1])
print("IZQ / DER / agita o boca arriba-abajo = ANOMALIA")

# 3) En vivo: cluster cercano = ángulo del servo; lejos o vibrar = centro
while True:
    p, vib = leer()
    cm = distancia_cm()
    d0 = dist(p, centros[0])
    d1 = dist(p, centros[1])
    if d0 <= d1:
        idx, menor = 0, d0        # cluster más cercano
    else:
        idx, menor = 1, d1
    if 2 < cm < LIMITE_CM:
        parar()
        paradas += 1
        print("STOP ultrasónico", round(cm, 1), "cm")
    elif menor > umbral or vib > umbral_vib:
        parar()                   # boca arriba/abajo o agitar: no es izq ni der
        paradas += 1
        print("ANOMALIA dist=", round(menor, 3), "vib=", round(vib, 3), "STOP")
    else:
        producir(etiqueta[idx])   # IZQ o DER según el cluster
        ok += 1
        print(etiqueta[idx], "dist=", round(menor, 3), "ax=", round(p[0], 2), "ay=", round(p[1], 2))
    sleep(0.3)
