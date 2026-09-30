import bluetooth
import struct

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE,
)

_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

class BLEUART:

    def __init__(self, name="ESP32"):

        self.ble = bluetooth.BLE()
        self.ble.active(True)

        self.connections = set()

        self.ble.irq(self._irq)

        ((self.tx, self.rx),) = self.ble.gatts_register_services((_UART_SERVICE,))

        self._advertise(name)

    def _irq(self, event, data):

        if event == 1:
            conn, _, _ = data
            self.connections.add(conn)
            print("Conectado")

        elif event == 2:
            conn, _, _ = data

            if conn in self.connections:
                self.connections.remove(conn)

            print("Desconectado")
            self._advertise()

        elif event == 3:
            value = self.ble.gatts_read(self.rx)

            print("RX:", value)

    def send(self, text):

        if isinstance(text, str):
            text = text.encode()

        for conn in self.connections:
            self.ble.gatts_notify(conn, self.tx, text)

    def _advertise(self, name):

        payload = bytearray()

        payload += struct.pack("BB",2,0x01)
        payload += b'\x06'

        name = name.encode()

        payload += struct.pack("BB",len(name)+1,0x09)
        payload += name

        self.ble.gap_advertise(100000,payload)