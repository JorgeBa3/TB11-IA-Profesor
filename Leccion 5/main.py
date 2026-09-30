from machine import Pin, PWM, SoftI2C
from mpu6050 import MPU6050
from utime import sleep
import math

# Importar librerías y configurar pines
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
    return (abs(ax), abs(math.sqrt(ax**2 + ay**2 + az**2) - 1))

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def kmeans(datos, k):
    n = len(datos)
    if k > n:
        k = n
    centros = [datos[i * n // k] for i in range(k)]
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
    umbral = max(min(dist(p, c) for c in centros) for p in datos) * 1.5
    llenos = sum(1 for g in grupos if g)
    return centros, umbral, llenos

def etiqueta(p, centros, umbral):
    d = [dist(p, c) for c in centros]
    menor = min(d)
    if menor > umbral:
        return "ANOMALIA", menor
    return "grupo " + str(d.index(menor)), menor

# 1) Recolectar CSV en la ESP32 (sin etiquetas)
archivo = open("datos.csv", "w")
archivo.write("inclinacion,vibracion\n")
for modo in modos:
    print("Pon el MPU6050:", modo)
    sleep(3)
    for i in range(5):
        p = leer()
        archivo.write("{:.3f},{:.3f}\n".format(p[0], p[1]))
        print(i + 1, round(p[0], 2), round(p[1], 2))
        sleep(0.3)
archivo.close()

# 2) Tres modelos: sesgo, el que generaliza, sobreajuste
datos = []
archivo = open("datos.csv")
archivo.readline()
for linea in archivo:
    a, b = linea.strip().split(",")
    datos.append((float(a), float(b)))
archivo.close()

sesgo = kmeans(datos, 1)
ok = kmeans(datos, 3)
memoria = kmeans(datos, len(datos))
print("K=1 sesgo:          grupos=", sesgo[2], " umbral=", round(sesgo[1], 3))
print("K=3 generaliza:     grupos=", ok[2], " umbral=", round(ok[1], 3))
print("K grande sobreajuste: grupos=", memoria[2], " umbral=", round(memoria[1], 3))
print("LED/buzzer siguen a K=3. Mira la consola: K=1 no distingue, K grande alerta de mas.")

# 3) En vivo: los tres a la vez; actuadores = K=3
while True:
    p = leer()
    t1, d1 = etiqueta(p, sesgo[0], sesgo[1])
    t3, d3 = etiqueta(p, ok[0], ok[1])
    tg, dg = etiqueta(p, memoria[0], memoria[1])
    if t3 == "ANOMALIA":
        led.on()
        buzzer.freq(2000)
        buzzer.duty(512)
    else:
        led.off()
        buzzer.duty(0)
    print("K1", t1, "| K3", t3, "| Kgrande", tg)
    sleep(0.3)
