import network
import time

wlan = network.WLAN(network.STA_IF)

wlan.active(False)
time.sleep(1)

wlan.active(True)

print("WiFi activo:", wlan.active())

print("Escaneando...")

redes = wlan.scan()

for r in redes:
    print(r[0].decode(), "RSSI:", r[3])