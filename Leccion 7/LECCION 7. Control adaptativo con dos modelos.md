LECCIÓN 7. Optimización en tiempo real: control adaptativo con dos modelos

INTRODUCCIÓN

Hoy aprenderás a **combinar dos modelos de inteligencia artificial para que tomen una decisión juntos, en tiempo real**. Una fábrica moderna no se queda con una sola pregunta. Un modelo responde “¿en qué modo está la línea?” y otro responde “¿cuánta energía corresponde ahora?”. Después una regla simple elige qué hacer: bajar el consumo, mantenerlo o parar si algo es raro. En las lecciones anteriores ya entrenaste esas dos piezas por separado: el clustering de la lección 4 y la recta de la lección 3. Hoy las corres las dos en la ESP32, pero con un sensor distinto: el ultrasónico de la lección 1. Así no vuelves a armar el acelerómetro. Los tres modos son CERCA, MEDIO y LEJOS, como una pieza en la banda. Si el clustering ve una anomalía (un cuarto lugar, o tapar el sensor), priorizas la seguridad: LED apagado y buzzer. Si el modo es normal, el brillo del LED sigue a la recta: más cerca, más “consumo” de la estación. Comprenderás cómo esta práctica contribuye al **ODS 9: Industria, innovación e infraestructura** y al **ODS 12: Producción y consumo responsables**, porque optimizar el modo y el consumo al mismo tiempo reduce energía y desperdicio, sin esperar a que una persona mire cada sensor.

PUNTO DE PARTIDA

¿Cómo tomaría decisiones inteligentes una fábrica si tuviera que considerar varias predicciones al mismo tiempo?

CONCEPTOS IMPORTANTES

**Control adaptativo:** Es un sistema que cambia su acción según lo que está pasando ahora, no con una sola regla rígida. En la práctica el LED no está solo encendido o apagado: su brillo sube o baja con el consumo que predice la recta, y se apaga del todo si hay anomalía. En la industria, una estación de ensamblaje baja velocidad cuando la pieza está lejos y para si aparece un objeto donde no debería.

**Múltiples modelos:** Cada modelo responde una pregunta distinta. El clustering responde “¿qué modo?” (una categoría: CERCA, MEDIO, LEJOS o ANOMALÍA). La regresión responde “¿cuánto?” (un número: el consumo estimado según la distancia). En una fábrica no usas un solo cerebro: un modelo mira si hay pieza en la zona de trabajo y otro estima la energía; los dos alimentan la misma decisión.

**Regla de decisión:** Es el “optimizador” simple que combina las dos salidas. En la práctica: si hay anomalía, gana la seguridad (buzzer y LED en 0). Si no, el LED usa el valor de la recta. En la industria, si el detector de rarezas alerta, no se acelera la línea aunque el predictor de demanda pida más producción: primero se protege la máquina y a las personas.

**Tiempo real:** Es el ciclo leer → predecir → actuar, una y otra vez, en milisegundos, dentro del microcontrolador. No se espera a bajar un CSV a la computadora para decidir. En una planta eso ocurre 24/7: cada eco del ultrasónico entra a los modelos y sale una orden a una luz, una alarma o, más adelante, un motor.

**Generalizar la decisión:** No basta con que cada modelo “acierte” por su lado. La decisión tiene que servir con distancias que no son exactamente las 15 filas del CSV. En la práctica pones la mano a 12 cm o a 28 cm: el clustering sigue reconociendo el modo y la recta entrega un brillo intermedio. En la industria, el martes la pieza no está en el milímetro del lunes; el sistema igual tiene que ajustar consumo.

DATO STEAM

¿Sabías que en almacenes automáticos y líneas de empaque se combinan un sensor de distancia (ultrasónico o láser) con un modelo de demanda energética? Uno dice “hay un paquete en esta zona” (un modo). Otro estima cuánta corriente pide la estación según qué tan cerca está el paquete. Si de pronto el eco no parece ninguno de los modos entrenados (una persona cruzó, un objeto se cayó), no se aumenta la producción: se alerta. Tu ESP32 hace la versión de aula: clustering para el modo, recta para el consumo, y una regla que no se pelea con la seguridad.
