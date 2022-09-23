import typing

from .. import crc16
from .. import msg

Address = int


class ClientSocket:
    def __init__(self, dev, inter_frame_delay: int):
        self.dev = dev
        self.inter_frame_delay = inter_frame_delay

    def send_to(self, pdu: msg.MasterPDU, dest: Address):
        if not (0 <= dest < 247):
            raise ValueError(dest, "bad address")

        crc = crc16.CRC16()

        # must be idle for 3.5 chars for a clear-to-send (listen-before-talk)
        # must not pause for longer than 1.5 chars while sending (inter-byte-time) otherwise fail.
        # end of frame is 3.5 chars idle after last byte.
        self.dev.write(dest.to_bytes(1, byteorder="big", signed=False))
        crc.update_bytes(dest.to_bytes(1, byteorder="big", signed=False))

        if isinstance(pdu, msg.MasterReadRegMulti):
            self.dev.write((3).to_bytes(1, byteorder="big", signed=False))
            crc.update_bytes((3).to_bytes(1, byteorder="big", signed=False))
            b = pdu.begin.to_bytes(length=2, byteorder="big", signed=False)
            self.dev.write(b)
            crc.update_bytes(b)
            b = pdu.len.to_bytes(length=2, byteorder="big", signed=False)
            self.dev.write(b)
            crc.update_bytes(b)
        else:
            raise ValueError(pdu, "unknown pdu type")

        self.dev.write(
            crc.value().to_bytes(length=2, byteorder="little", signed=False)
        )

        self.dev.write(b"\x0d\x0a")
        self.dev.flushOutput()

        # must idle/not send for 3.5 chars after last byte for EndOfFrame.

    def recv(self) -> typing.Tuple[msg.SlavePDU, Address]:
        pass

    def sendrecv(self, pdu: msg.MasterPDU, dest: Address) -> msg.SlavePDU:
        pass
