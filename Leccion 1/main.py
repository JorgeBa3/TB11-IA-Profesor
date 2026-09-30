from machine import Pin, SoftI2C
from mpu6050 import MPU6050
from utime import sleep
import math

# Importar librerías y configurar pines
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
print("I2C scan:", i2c.scan())
mpu = MPU6050(i2c)
led = Pin(26, Pin.OUT)
in1 = Pin(19, Pin.OUT)        # LOZ derecha
in2 = Pin(18, Pin.OUT)        # LOZ izquierda
led.off()
in1.off()
in2.off()
modos = ["HORIZONTAL", "IZQUIERDA", "DERECHA"]

# Definir funciones
def leer():
    ax, ay, az, gx, gy, gz = mpu.leer()
    return (ax, ay)           # SIN abs: así se distingue izq, der y plano

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def kmeans(datos, k=3):
    n = len(datos)
    centros = [datos[0], datos[n // 3], datos[(2 * n) // 3]]
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
    return centros

def parar():
    in1.off()
    in2.off()
    led.off()

def derecha():
    in2.off()
    in1.on()
    led.on()

def izquierda():
    in1.off()
    in2.on()
    led.on()

def actuar(modo):
    if modo == "HORIZONTAL":
        parar()
    elif modo == "IZQUIERDA":
        izquierda()
    else:
        derecha()

# 1) Recolectar 3 estados: plano, ladeado izq, ladeado der
archivo = open("datos.csv", "w")
archivo.write("ax,ay\n")
grupos = {"HORIZONTAL": [], "IZQUIERDA": [], "DERECHA": []}
for modo in modos:
    print("Pon el MPU6050:", modo, "y mantenlo")
    sleep(3)
    for i in range(5):
        p = leer()
        grupos[modo].append(p)
        archivo.write("{:.3f},{:.3f}\n".format(p[0], p[1]))
        print(i + 1, "ax=", round(p[0], 2), "ay=", round(p[1], 2))
        sleep(0.3)
archivo.close()

# 2) K-means K=3 y nombra cada centro con lo que guardaste
datos = grupos["HORIZONTAL"] + grupos["IZQUIERDA"] + grupos["DERECHA"]
centros = kmeans(datos)
medias = {}
for modo in modos:
    pts = grupos[modo]
    medias[modo] = (
        sum(p[0] for p in pts) / 5,
        sum(p[1] for p in pts) / 5,
    )
etiqueta = []
usados = []
for c in centros:
    cand = sorted(modos, key=lambda m: dist(c, medias[m]))
    for m in cand:
        if m not in usados:
            etiqueta.append(m)
            usados.append(m)
            break
print("centros:", etiqueta[0], centros[0], etiqueta[1], centros[1], etiqueta[2], centros[2])
print("En vivo: plano=para  izq/der=gira el LOZ")

# 3) El cluster mas cercano mueve el LOZ
while True:
    p = leer()
    d0 = dist(p, centros[0])
    d1 = dist(p, centros[1])
    d2 = dist(p, centros[2])
    idx = [d0, d1, d2].index(min(d0, d1, d2))
    modo = etiqueta[idx]
    actuar(modo)
    print(modo, "ax=", round(p[0], 2), "ay=", round(p[1], 2))
    sleep(0.2)
