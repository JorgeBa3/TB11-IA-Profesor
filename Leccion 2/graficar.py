import math
import pandas as pd
import matplotlib.pyplot as plt

# Baja datos.csv de la ESP32 a esta carpeta y corre: python graficar.py
df = pd.read_csv("datos.csv")
ang = df["angulo"].tolist()
luz = df["luz"].tolist()
cm = df["cm"].tolist()
theta = [a * math.pi / 180.0 for a in ang]

fig = plt.figure(figsize=(11, 5))

radar = fig.add_subplot(1, 2, 1, projection="polar")
radar.plot(theta, cm, marker="o", color="#2e6da4")
radar.set_title("Radar: distancia (cm)")
radar.set_thetamin(0)
radar.set_thetamax(180)

lineas = fig.add_subplot(1, 2, 2)
lineas.plot(ang, cm, marker="o", color="#2e6da4", label="distancia (cm)")
ax_luz = lineas.twinx()
ax_luz.plot(ang, luz, marker="s", color="#d9534f", label="luz (%)")
lineas.set_xlabel("ángulo (°)")
lineas.set_ylabel("distancia (cm)", color="#2e6da4")
ax_luz.set_ylabel("luz (%)", color="#d9534f")
lineas.set_title("Luz y distancia por ángulo")
lineas.grid(True, linestyle="--", alpha=0.5)
lineas.legend(loc="upper left")
ax_luz.legend(loc="upper right")

plt.tight_layout()
plt.show()
