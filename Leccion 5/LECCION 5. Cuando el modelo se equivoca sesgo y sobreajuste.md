LECCIÓN 5. Cuando el modelo se equivoca: sesgo y sobreajuste

INTRODUCCIÓN

Hoy aprenderás a **reconocer cuándo un modelo de inteligencia artificial falla por ser demasiado simple o por memorizar de más**. En la lección anterior entrenaste un clustering con K = 3 y viste tres modos de la máquina: HORIZONTAL, INCLINADO y DE LADO. Hoy vas a usar esos mismos datos, pero cambiando K, para descubrir dos errores clásicos. Si el modelo es demasiado simple, trata todos los modos como si fueran uno solo: eso es sesgo. Si es demasiado complejo, memoriza cada fila del CSV, incluido el temblor del sensor, y con un dato nuevo ya no reconoce nada: eso es sobreajuste. En una fábrica real, el primero no distingue producción de mantenimiento; el segundo para la línea por alarmas falsas. El objetivo no es acertar el 100% del entrenamiento, sino generalizar a datos que el modelo nunca vio. Comprenderás cómo esta práctica contribuye al **ODS 9: Industria, innovación e infraestructura** y al **ODS 12: Producción y consumo responsables**, porque un modelo mal ajustado desperdicia material, energía y tiempo de máquina, y uno bien ajustado previene fallas sin detener la producción a cada rato.

PUNTO DE PARTIDA

¿Por qué un modelo que acierta todo en el entrenamiento puede fallar al día siguiente en la fábrica?

CONCEPTOS IMPORTANTES

**Sesgo:** Es el error de un modelo demasiado simple, que no alcanza a capturar el patrón real. En la práctica vas a entrenar K-means con K = 1: un solo centro para las tres poses. Horizontal, inclinado y de lado saldrán como el mismo modo. En la industria, un modelo de mantenimiento entrenado como si todas las máquinas fueran iguales no distingue una línea lenta de una rápida, y nunca recomienda el ajuste correcto.

**Sobreajuste (overfitting):** Es cuando el modelo memoriza los datos de entrenamiento tan bien, incluido el ruido, que no funciona con datos nuevos. En la práctica, si usas un K casi igual al número de filas del CSV, cada muestra se vuelve su propio grupo. Un temblor mínimo del MPU6050 ya no encaja y el sistema grita anomalía. En una fábrica, un modelo que memoriza cada pico de un sensor ruidoso dispara alarmas falsas y detiene la línea sin que haya una falla real.

**Subajuste:** Es la pareja del sesgo: el modelo se queda corto y no aprendió lo suficiente. K = 1 es un subajuste: ni siquiera separa los tres modos que tú creaste a propósito. En la industria ocurre cuando se usa una regla demasiado burda, por ejemplo “si hay vibración, hay falla”, y se ignoran los modos normales de operación.

**Generalizar:** Es acertar con datos que no estaban en el entrenamiento. El K = 3 de la lección 4 generaliza: si vuelves a poner el sensor casi horizontal, el modelo lo reconoce aunque esa fila exacta no esté en el CSV. En una fábrica, generalizar significa que el modelo sigue sirviendo el martes con una máquina un poco más caliente, no solo con las 15 mediciones del lunes.

**Datos de entrenamiento vs datos nuevos:** Los de entrenamiento son el CSV que guardas en la ESP32 (las 15 muestras de las tres poses). Los datos nuevos son lo que haces después: inclinar otra vez, poner de lado o agitar. Si el modelo solo funciona con las filas memorizadas, está sobreajustado. Si ni siquiera separa las tres poses del CSV, tiene sesgo. En la industria se reserva una parte de los datos solo para probar, precisamente para no confiar en un modelo que “se sabe el examen de memoria”.

DATO STEAM

¿Sabías que muchas alarmas falsas en plantas industriales no vienen de un sensor roto, sino de un modelo sobreajustado? El modelo se entrenó con una semana de datos tan al detalle que aprendió el ruido de ese edificio, esa humedad y ese turno. Al mes siguiente, con otro clima o otra velocidad de línea, todo le parece “raro” y para la producción. El caso contrario también existe: un modelo demasiado simple (sesgo) que nunca alerta, porque redujo toda la fábrica a un solo “modo normal”. Por eso los equipos de IA no buscan el 100% de acierto en el entrenamiento: buscan el punto medio, el que generaliza. Tu práctica de hoy hace exactamente eso, pero a escala de aula: K = 1 se queda corto, K grande memoriza, y K = 3 es el que sí sirve cuando mueves el sensor de verdad.
