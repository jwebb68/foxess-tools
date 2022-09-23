"""
A script to emit a fixed string to a serial port, at foxess bms batt rs485 baud rate,
with a pause between emissions.

To simulate a modbus packet with it's inter-packet pauses, so s/w on  arduino can
be developed and tested in isolation.

"""

import datetime
import time

import serial


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
        samp = "0123456789abcdef\n".encode()
        while True:
            dev.write(samp)
            dev.flush()
            print(
                datetime.datetime.utcnow().time().isoformat("milliseconds"),
                "->",
                "*<",
                f"{len(samp)}: {samp.hex(' ')}",
            )
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
