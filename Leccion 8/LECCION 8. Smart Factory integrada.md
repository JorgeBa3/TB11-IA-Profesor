LECCIÓN 8. Smart Factory integrada: convergencia de electrónica e IA

INTRODUCCIÓN

Hoy **vas a convertir lo que ya construiste en una mini fábrica inteligente**. En la lección 7 el cerebro ya combinaba dos modelos: clustering (¿qué modo?) y una recta (¿cuánto consumo?). Hoy ese cerebro mueve un mecanismo de verdad: un servo es el brazo clasificador de la línea y un ultrasónico vigila si hay una pieza o una persona demasiado cerca. No es un modelo nuevo. Es arquitectura: los datos salen de varios sensores, pasan por los modelos, una regla decide y los actuadores responden. Si el MPU6050 ve una anomalía, el brazo vuelve al centro. Si el ultrasónico ve un obstáculo, también: un solo sensor no es suficiente para confiar, y dos formas de frenar hacen la fábrica más segura. Comprenderás cómo esta práctica contribuye al **ODS 7: Energía asequible y no contaminante**, al **ODS 9: Industria, innovación e infraestructura** y al **ODS 12: Producción y consumo responsables**, porque un sistema integrado ahorra energía cuando puede clasificar, y evita accidentes y desperdicio cuando tiene que parar.

PUNTO DE PARTIDA

¿Cómo conviertes varios sensores, dos modelos y unos actuadores en una sola fábrica que se coordina sola?

CONCEPTOS IMPORTANTES

**Pipeline:** Es la tubería por la que pasan los datos: leer sensores → limpiar/usar el CSV → predicción de los modelos → regla de decisión → acción (servo, LED, buzzer). Si un paso falla, se detiene todo. En la práctica tu `main.py` sigue exactamente ese orden. En la industria, si se cae la lectura de un sensor o un modelo no responde, hay que diseñar qué hace la línea: ir a una posición segura es más seguro que seguir a ciegas.

**Redundancia y tolerancia a fallos:** Es no fiarse de un solo sensor. En la práctica el MPU6050 dice si el “modo de la máquina” es raro y el ultrasónico dice si hay un obstáculo en la banda. Cualquiera de los dos puede mandar el servo al centro. En una fábrica real, si un acelerómetro falla o se desconecta, una cortina de luz o un ultrasónico sigue protegiendo a las personas. Una fábrica inteligente no es más inteligente si es frágil.

**Métrica de desempeño global:** No basta con preguntar “¿acertó el modelo?”. Hay que preguntar qué logró la fábrica: ¿cuántos ciclos clasificó? ¿cuántas veces paró por seguridad? En la práctica la consola cuenta ciclos OK y paradas. En la industria se mira energía no desperdiciada, piezas buenas y tiempo de línea detenida: eso vale más que un 99% de acierto en un CSV.

**Mejora continua:** El sistema no se deja estático. Si el ultrasónico para demasiado (el umbral de 15 cm quedó corto o largo), o el clustering alerta de más, se ajusta el umbral o se vuelve a recolectar el CSV. En la industria, si una predicción salió mal se pregunta: ¿faltó un sensor? ¿hay que reentrenar? Los sistemas reales se revisan, no se graban una vez y se olvidan.

**Control de la línea:** El servo es el brazo clasificador. GPIO 18 solo manda un pulso PWM a 50 Hz (el ancho del pulso es el ángulo); la fuerza la da el 5V, no el pin. El clustering reconoce dos poses: IZQUIERDA mueve el brazo a 45° y DERECHA a 135°. Boca arriba, boca abajo o agitar es anomalía: el servo va a 90° (centro) y suena el buzzer. El ultrasónico suma la misma posición segura si hay un obstáculo real. En una planta, el mismo principio desvía la pieza a un lado u otro, o no clasifica si algo está mal.

DATO STEAM

¿Sabías que en una línea automotriz un brazo o un desviador no se mueve por un solo número? Hay redundancia a propósito: un sensor de visión, un ultrasónico o una cortina de luz pueden pedir posición segura aunque el modelo de vibración diga “todo normal”, y al revés. Después el tablero no presume aciertos del algoritmo: muestra OEE, paros y piezas por hora. Tu mini fábrica hace lo mismo a escala de protoboard: dos modelos, dos sensores, un servo, y una cuenta de cuántas veces clasificó y cuántas veces protegió.
