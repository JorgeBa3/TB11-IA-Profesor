from machine import Pin, PWM, SoftI2C
from mpu6050 import MPU6050
from utime import sleep
import math

# Importar librerías y configurar pines
# SDA=21  SCL=22  LED=26  Buzzer=25
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
print("I2C scan:", i2c.scan())
mpu = MPU6050(i2c)
led = Pin(26, Pin.OUT)
buzzer = PWM(Pin(25))
buzzer.duty(0)
modos = ["HORIZONTAL", "INCLINADO", "DE LADO"]

# Definir funciones
def leer():
    ax, ay, az, gx, gy, gz = mpu.leer()
    inclinacion = abs(ax)
    vibracion = abs(math.sqrt(ax**2 + ay**2 + az**2) - 1)
    return (inclinacion, vibracion)

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

# 1) Datos SIN etiquetas -> CSV en la ESP32
archivo = open("datos.csv", "w")
archivo.write("inclinacion,vibracion\n")
for modo in modos:
    print("Pon el MPU6050 como", modo)
    sleep(3)
    for i in range(5):
        p = leer()
        archivo.write("{:.3f},{:.3f}\n".format(p[0], p[1]))
        print(i + 1, round(p[0], 2), round(p[1], 2))
        sleep(0.3)
archivo.close()
print("CSV en la ESP32: datos.csv")

# 2) K-means a mano: 3 centros, asigna, recalcula
datos = []
archivo = open("datos.csv")
archivo.readline()
for linea in archivo:
    a, b = linea.strip().split(",")
    datos.append((float(a), float(b)))
archivo.close()

centros = [datos[0], datos[5], datos[10]]
for _ in range(8):
    grupos = [[], [], []]
    for p in datos:
        d = [dist(p, c) for c in centros]
        grupos[d.index(min(d))].append(p)
    for i in range(3):
        if grupos[i]:
            mx = sum(p[0] for p in grupos[i]) / len(grupos[i])
            my = sum(p[1] for p in grupos[i]) / len(grupos[i])
            centros[i] = (mx, my)

umbral = max(min(dist(p, c) for c in centros) for p in datos) * 1.5
print("3 modos descubiertos (sin etiquetas):")
for i in range(3):
    print(" ", modos[i], "n=", len(grupos[i]), "centro=", centros[i])
print("Umbral de anomalia:", round(umbral, 3))
print("Agita fuerte = 4to modo = ANOMALIA")

# 3) En vivo: grupo cercano o alerta
while True:
    p = leer()
    d = [dist(p, c) for c in centros]
    menor = min(d)
    if menor > umbral:
        led.on()
        buzzer.freq(2000)
        buzzer.duty(512)
        print("ANOMALIA dist=", round(menor, 3))
    else:
        led.off()
        buzzer.duty(0)
        print(modos[d.index(menor)], "dist=", round(menor, 3))
    sleep(0.3)
