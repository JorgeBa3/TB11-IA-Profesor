from machine import Pin, PWM
from utime import sleep

# Señal en GPIO 18. VCC del servo a 5V, GND común. Nunca alimentes el servo por el GPIO.
servo = PWM(Pin(18), freq=50)

def angulo(g):
    us = 500 + (g / 180.0) * 2000
    servo.duty_u16(int(us / 20000.0 * 65535))

print("Prueba servo GPIO 18")
print("IZQ 45 / centro 90 / DER 135")

while True:
    print("IZQ 45")
    angulo(45)
    sleep(2)
    print("centro 90")
    angulo(90)
    sleep(2)
    print("DER 135")
    angulo(135)
    sleep(2)
