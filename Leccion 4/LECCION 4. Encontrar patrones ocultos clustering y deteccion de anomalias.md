LECCIÓN 4. Encontrar patrones ocultos: clustering y detección de anomalías

Descripción: Con este programa aprenderás a recolectar datos de una máquina sin etiquetas, guardarlos en un archivo datos.csv dentro de la ESP32 y entrenar un modelo de clustering K-means a mano. El modelo descubre tres modos: HORIZONTAL, INCLINADO y DE LADO. Si aparece un cuarto modo raro (agitar el sensor), lo detecta como anomalía y alerta con LED y buzzer.

Electrónica:

Materiales:
ESP32
Protoboard
MPU6050 (acelerómetro)
LED
Resistencia 220 Ω
Buzzer
Cables jumper

Paso 1: Coloca el MPU6050 en el protoboard y conéctalo a la ESP32.
VCC → 3V3
GND → GND
SDA → GPIO 21
SCL → GPIO 22

Paso 2: En el mismo protoboard conecta el LED y el buzzer. Luego conecta la ESP32 a tu computadora.
LED: GPIO 26 → resistencia 220 Ω → pata larga del LED (+)
Pata corta del LED (−) → GND
Buzzer: GPIO 25 → pata (+) del buzzer
Pata (−) del buzzer → GND

Programación:
Sube a la ESP32 los archivos main.py y mpu6050.py.

Importar librerías y configurar pines:
Importa Pin, PWM, SoftI2C, MPU6050, sleep y math. Configura I2C en GPIO 21 (SDA) y GPIO 22 (SCL), el LED en GPIO 26 y el buzzer en GPIO 25. Los tres modos son HORIZONTAL, INCLINADO y DE LADO.

Definir funciones:
leer() obtiene inclinación y vibración del MPU6050. dist() calcula la distancia euclidiana entre dos puntos. En una fábrica esas variables serían temperatura y vibración; aquí las creas moviendo el sensor.

# 1) Recolectar datos sin etiquetas y guardarlos en datos.csv dentro de la ESP32. Cuando la consola pida cada modo, coloca el MPU6050 así:
HORIZONTAL: plano, en reposo
INCLINADO: inclinado
DE LADO: de lado
Guarda 5 muestras de cada uno. El CSV solo tiene inclinacion,vibracion. No guarda el nombre del modo.

# 2) Leer el CSV y entrenar K-means a mano (K = 3). El programa elige 3 centros, asigna cada punto al más cercano con distancia euclidiana y recalcula los centros. Repite hasta que dejen de moverse. Así responde la pregunta de esta lección: ¿cómo podría una máquina saber qué es “anormal” si nadie le mostró ejemplos de fallas?

# 3) Usar el modelo en vivo. Cada lectura nueva se compara con los 3 centros. Si está cerca, la consola muestra HORIZONTAL, INCLINADO o DE LADO. Si está muy lejos (un cuarto modo raro), enciende el LED y el buzzer: ANOMALÍA. Para probarlo, agita fuerte el MPU6050.

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB11/Leccion%204
