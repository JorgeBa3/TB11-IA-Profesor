LECCIÓN 5. Cuando el modelo se equivoca: sesgo y sobreajuste

Descripción: Con este programa aprenderás a recolectar tus propios datos en la ESP32 y a entrenar el mismo K-means tres veces, cambiando K. K = 1 es sesgo (un solo grupo). K = 3 generaliza (los tres modos de la lección 4). K grande es sobreajuste (casi un grupo por fila del CSV). En vivo comparas las tres salidas: el LED y el buzzer siguen a K = 3; la consola te muestra cómo K = 1 no distingue y cómo K grande alerta de más.

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
Importa Pin, PWM, SoftI2C, MPU6050, sleep y math. Configura I2C en GPIO 21 (SDA) y GPIO 22 (SCL), el LED en GPIO 26 y el buzzer en GPIO 25.

Definir funciones:
leer() obtiene inclinación y vibración. dist() es la distancia euclidiana. kmeans(datos, k) agrupa a mano y calcula el umbral de anomalía. etiqueta() dice si el punto es un grupo o ANOMALÍA.

# 1) Recolectar datos sin etiquetas y guardarlos en datos.csv dentro de la ESP32. Cuando la consola pida cada modo, coloca el MPU6050 así:
HORIZONTAL: plano, en reposo
INCLINADO: inclinado
DE LADO: de lado
Guarda 5 muestras de cada uno. Ese CSV es tu conjunto de entrenamiento. Nota: el archivo tiene que salir de TU sensor, para que el entrenamiento y la prueba en vivo usen los mismos números. Si el MPU6050 no se detecta, sube el CSV de apoyo de la biblioteca de recursos y nómbralo datos.csv; en ese caso compara K en consola, sin demo en vivo.

# 2) Leer el CSV y entrenar tres modelos. K = 1 (sesgo): un solo centro, las tres poses parecen el mismo modo. K = 3 (generaliza): el de la lección 4. K grande (sobreajuste): tantos grupos como filas, el modelo memoriza el CSV. Mira los umbrales: el de K grande sale casi 0.

# 3) Usar los tres en vivo. Mueve el sensor como en la lección 4 y luego agítalo. La consola imprime K1 | K3 | Kgrande. El LED y el buzzer siguen solo a K = 3. Así respondes la pregunta de esta lección: ¿por qué un modelo que acierta todo en el entrenamiento puede fallar al día siguiente en la fábrica?

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB11/Leccion%205
