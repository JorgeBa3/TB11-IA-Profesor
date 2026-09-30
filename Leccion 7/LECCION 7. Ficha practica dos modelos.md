LECCIÓN 7. Optimización en tiempo real: control adaptativo con dos modelos

Descripción: Con este programa aprenderás a recolectar tus datos en la ESP32 con el sensor ultrasónico y a entrenar dos modelos a mano: K-means (¿qué modo: CERCA, MEDIO o LEJOS?) y una recta de regresión (¿cuánto consumo?). Una regla combina las dos salidas. Si el clustering ve anomalía, el buzzer suena y el LED se apaga. Si el modo es normal, el brillo del LED sigue a la recta. El CSV tiene que salir de TU ultrasónico.

Electrónica:

Materiales:
ESP32
Protoboard
Sensor ultrasónico HC-SR04
LED
Resistencia 220 Ω
Buzzer
Cables jumper

Paso 1: Coloca el ultrasónico en el protoboard y conéctalo a la ESP32.
VCC → 5V
GND → GND
TRIG → GPIO 4
ECHO → GPIO 5
(Si tu HC-SR04 es de 5 V en ECHO, usa el divisor o el módulo que ya trae el kit.)

Paso 2: En el mismo protoboard conecta el LED y el buzzer. Luego conecta la ESP32 a tu computadora.
LED: GPIO 26 → resistencia 220 Ω → pata larga del LED (+)
Pata corta del LED (−) → GND
Buzzer: GPIO 25 → pata (+) del buzzer
Pata (−) del buzzer → GND

Programación:
Sube a la ESP32 el archivo main.py (en esta lección no usas mpu6050.py).

Importar librerías y configurar pines:
Importa Pin, PWM, ticks_us, sleep y math. TRIG en GPIO 4, ECHO en GPIO 5. El LED y el buzzer van en PWM: GPIO 26 y GPIO 25. Los modos son CERCA, MEDIO y LEJOS.

Definir funciones:
distancia_cm() mide el eco. leer() guarda distancia y un consumo estimado (más cerca, más consumo de la estación). dist() es la distancia euclidiana. kmeans() descubre los 3 modos. recta() calcula m y b: consumo = m × distancia + b.

# 1) Recolectar datos sin etiquetas y guardarlos en datos.csv dentro de la ESP32. Cuando la consola pida cada modo, coloca la mano o un objeto así:
CERCA: unos 10 cm
MEDIO: unos 25 cm
LEJOS: unos 40 cm
Guarda 5 muestras de cada uno. El CSV tiene distancia,consumo.

# 2) Leer el CSV y entrenar los dos modelos. K-means (K = 3) responde “¿qué modo?”. La recta responde “¿cuánto?”. Imprime centros, umbral, m y b.

# 3) En vivo, la regla de decisión. Cada lectura entra a los dos modelos. Si hay ANOMALÍA (tapar el sensor o un cuarto lugar), LED en 0 y buzzer. Si no, el PWM del LED sigue la recta (más cerca, más brillo). Recorre las tres distancias y al final tapa el sensor. Así respondes: ¿cómo decide una fábrica si tiene que mirar el modo y el consumo al mismo tiempo?

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB11/Leccion%207
