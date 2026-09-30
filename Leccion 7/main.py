from machine import Pin, PWM
from utime import sleep, ticks_us, ticks_diff
import math

# Importar librerías y configurar pines
trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)
led = PWM(Pin(26))
buzzer = PWM(Pin(25))
led.duty(0)
buzzer.duty(0)
modos = ["CERCA", "MEDIO", "LEJOS"]

# Definir funciones
def distancia_cm():
    trig.off()
    sleep(0.00001)
    trig.on()
    sleep(0.00001)
    trig.off()
    t0 = ticks_us()
    while echo.value() == 0:
        if ticks_diff(ticks_us(), t0) > 30000:
            return 400.0
        t_ini = ticks_us()
    t0 = ticks_us()
    while echo.value() == 1:
        if ticks_diff(ticks_us(), t0) > 30000:
            return 400.0
        t_fin = ticks_us()
    return (ticks_diff(t_fin, t_ini) * 0.0343) / 2

def leer():
    d = distancia_cm()
    consumo = max(0, 80 - d)
    return (d, consumo)

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def kmeans(datos, k=3):
    n = len(datos)
    centros = [datos[i * n // k] for i in range(k)]
    for _ in range(8):
        grupos = [[] for _ in range(k)]
        for p in datos:
            ds = [dist(p, c) for c in centros]
            grupos[ds.index(min(ds))].append(p)
        for i in range(k):
            if grupos[i]:
                mx = sum(p[0] for p in grupos[i]) / len(grupos[i])
                my = sum(p[1] for p in grupos[i]) / len(grupos[i])
                centros[i] = (mx, my)
    umbral = max(min(dist(p, c) for c in centros) for p in datos) * 1.5
    return centros, umbral

def recta(datos):
    n = len(datos)
    sx = sum(p[0] for p in datos)
    sy = sum(p[1] for p in datos)
    den = n * sum(p[0] * p[0] for p in datos) - sx * sx
    if den == 0:
        return 0.0, sy / n
    m = (n * sum(p[0] * p[1] for p in datos) - sx * sy) / den
    return m, (sy - m * sx) / n

# 1) Recolectar CSV en la ESP32 (sin etiquetas)
archivo = open("datos.csv", "w")
archivo.write("distancia,consumo\n")
for modo in modos:
    print("Pon la mano:", modo, "(cerca ~10cm, medio ~25cm, lejos ~40cm)")
    sleep(3)
    for i in range(5):
        p = leer()
        archivo.write("{:.1f},{:.1f}\n".format(p[0], p[1]))
        print(i + 1, round(p[0], 1), "cm")
        sleep(0.3)
archivo.close()

# 2) Dos modelos: clustering (modo) + recta (consumo)
datos = []
archivo = open("datos.csv")
archivo.readline()
for linea in archivo:
    a, b = linea.strip().split(",")
    datos.append((float(a), float(b)))
archivo.close()

centros, umbral = kmeans(datos, 3)
m, b = recta(datos)
ymax = max(p[1] for p in datos)
if ymax < 1:
    ymax = 1
print("K-means umbral=", round(umbral, 2), "centros=", centros)
print("Recta: consumo = {:.3f} * distancia + {:.2f}".format(m, b))

# 3) Regla: anomalia -> alarma; si no, LED segun la recta
while True:
    p = leer()
    ds = [dist(p, c) for c in centros]
    menor = min(ds)
    pred = m * p[0] + b
    duty = int(min(1023, max(0, pred / ymax * 1023)))
    if menor > umbral:
        led.duty(0)
        buzzer.freq(2000)
        buzzer.duty(512)
        print("ANOMALIA cm=", round(p[0], 1))
    else:
        buzzer.duty(0)
        led.duty(duty)
        print(modos[ds.index(menor)], round(p[0], 1), "cm  consumo=", round(pred, 1), "LED=", duty)
    sleep(0.3)
