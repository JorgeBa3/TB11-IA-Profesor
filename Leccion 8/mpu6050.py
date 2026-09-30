from machine import I2C
import struct

class MPU6050:

    def __init__(self, i2c, addr=None):
        self.i2c = i2c
        encontrados = i2c.scan()
        if addr is None:
            if 0x68 in encontrados:
                addr = 0x68
            elif 0x69 in encontrados:
                addr = 0x69
            else:
                print("MPU6050 no encontrado. I2C scan:", encontrados)
                print("Revisa protoboard: VCC=3V3  GND=GND  SDA=21  SCL=22")
                raise OSError("ENODEV MPU6050")
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def leer(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        ax = struct.unpack(">h", data[0:2])[0]
        ay = struct.unpack(">h", data[2:4])[0]
        az = struct.unpack(">h", data[4:6])[0]
        gx = struct.unpack(">h", data[8:10])[0]
        gy = struct.unpack(">h", data[10:12])[0]
        gz = struct.unpack(">h", data[12:14])[0]
        return (
            ax / 16384,
            ay / 16384,
            az / 16384,
            gx / 131,
            gy / 131,
            gz / 131,
        )
