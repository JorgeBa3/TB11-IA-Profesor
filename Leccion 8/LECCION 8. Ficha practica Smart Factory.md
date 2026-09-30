LECCIÓN 8. Smart Factory integrada: convergencia de electrónica e IA

Descripción: Con este programa armarás una mini fábrica en el protoboard. Reusas el clustering de las lecciones anteriores. El MPU6050 guarda dos poses: inclinación a la izquierda e inclinación a la derecha. En vivo el K-means reconoce esas dos. Un servo es el brazo clasificador: IZQUIERDA → 45°, DERECHA → 135°, anomalía u obstáculo → 90° (centro, no clasifica). El LED muestra cuál modo es. El CSV sale de TU MPU6050.

Electrónica:

Materiales:
ESP32
Protoboard
MPU6050 (acelerómetro)
Sensor ultrasónico HC-SR04
LED
Resistencia 220 Ω
Buzzer
Servo (SG90 o equivalente)
Cables jumper
El servo se alimenta de 5V y GND. GPIO 18 solo lleva la señal PWM. Nunca alimentes el servo por un GPIO.

Paso 1: Coloca en el protoboard los sensores y conéctalos a la ESP32.
MPU6050: VCC → 3V3, GND → GND, SDA → GPIO 21, SCL → GPIO 22
Ultrasónico: VCC → 5V, GND → GND, TRIG → GPIO 4, ECHO → GPIO 5
(Si tu HC-SR04 es de 5 V en ECHO, usa el divisor o el módulo que ya trae el kit.)

Paso 2: Coloca los actuadores y el servo. Luego conecta la ESP32 a la computadora.
LED: GPIO 26 → 220 Ω → pata larga (+), pata corta → GND
Buzzer: GPIO 25 → (+), (−) → GND
Servo (tres cables):
Cable rojo (VCC) → 5V de la ESP32
Cable marrón o negro (GND) → GND
Cable naranja o amarillo (señal) → GPIO 18
Primero corre probar_servo.py: debe ir a 45°, 90° y 135°. Si gira al revés, cruza IZQ y DER en el código (ANG_IZQ / ANG_DER).

Programación:
Sube a la ESP32 los archivos main.py y mpu6050.py.

Importar librerías y configurar pines:
Importa Pin, PWM, SoftI2C, ticks_us, MPU6050, sleep y math. I2C 21/22, TRIG 4, ECHO 5, LED 26, buzzer 25, servo PWM GPIO 18 a 50 Hz.

Definir funciones:
leer() es ax y ay del MPU6050 (sin abs) y la vibración. distancia_cm() mide el ultrasónico. dist() y kmeans() son el clustering (K = 2). angulo() convierte 0–180° en pulso de 0.5–2.5 ms. parar() manda el servo a 90°. producir() manda 45° (IZQ) o 135° (DER). El LED cambia de brillo según el modo.

# 1) Recolectar datos.csv. Dos poses, 5 muestras cada una: IZQUIERDA y DERECHA. Inclina y mantén; no lo pongas boca arriba ni boca abajo.

# 2) Entrenar K-means (K = 2). Asigna cada centro a IZQ o DER según lo que guardaste. Imprime umbral de distancia y de vibración.

# 3) Pipeline en vivo. Cada ciclo: leer MPU6050 → cluster más cercano o ANOMALÍA → servo.
Si el punto está cerca de IZQUIERDA o DERECHA → el brazo va a ese lado. El LED indica el modo.
Si la distancia es mayor al umbral (boca arriba, boca abajo) o agitas → ANOMALÍA, servo al centro y buzzer.
Si el ultrasónico mide de verdad menos de 15 cm → parada de seguridad (centro).
La consola muestra IZQ, DER o ANOMALIA y la distancia al cluster.

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB11/Leccion%208
