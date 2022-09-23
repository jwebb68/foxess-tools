"""
read/write modbus messages over serial (presume connected to rs485 bus).

This uses a blocking method, which for multiple  ports would not work.

"""

import datetime
import sys
import time

import modbus
import serial

# from . import modbus


class SerialDebug:
    def __init__(self, dev):
        self.inner = dev

    def write(self, data: bytes):
        print("< ", data.hex(" "), file=sys.stderr)
        self.inner.write(data)

    def flushOutput(self):
        self.inner.flushOutput()

    @property
    def in_waiting(self):
        return self.inner.in_waiting

    def read(self, size=None):
        if size is None:
            data = self.inner.read()
        else:
            data = self.inner.read(size)
        print("> ", data.hex(" "), file=sys.stderr)
        return data


class SerialBuffer:
    def __init__(self, dev):
        self.inner = dev
        self.tx_buf = []
        self.rx_buf = []

    def write(self, data: bytes):
        self.tx_buf.append(data)

    def flushOutput(self):
        self.inner.write(b"".join(self.tx_buf))
        self.tx_buf = []
        self.inner.flushOutput()

    @property
    def in_waiting(self):
        return self.inner.in_waiting

    def read(self, size=None):
        if size is None:
            data = self.inner.read()
        else:
            data = self.inner.read(size)
        return data


def main():
    dev = serial.Serial(
        "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0PFU90-if00-port0",
        baudrate=115200,
        bytesize=8,
        parity=serial.PARITY_EVEN,
        # parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        # rtscts=True,
    )
    with dev:

        msg = modbus.msg.MasterReadRegMulti(begin=0x0120, len=2)
        dev = SerialDebug(dev)
        dev = SerialBuffer(dev)
        sock = modbus.rtu.ClientSocket(dev, 0)

        while True:
            sock.send_to(msg, 3)

            if dev.in_waiting > 0:
                inv = dev.read(dev.in_waiting)
                print(
                    datetime.datetime.utcnow().time().isoformat("milliseconds"),
                    "->",
                    "*>",
                    f"{len(inv)}: {inv.hex(' ')}",
                )

            time.sleep(1)


if __name__ == "__main__":
    main()
