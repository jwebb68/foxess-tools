class CRC16:
    def __init__(self, seed=0xFFFF):
        # crc internal is little endian
        # self.crc = ((seed & 0xff) << 8)|(seed & 0xff00) >> 8
        self.crc = seed & 0xFFFF

    def update_int(self, v: int):
        self.crc = self._update(self.crc, v)

    def update_bytes(self, seq: bytes):
        crc = self.crc
        for b in seq:
            crc = self._update(crc, b)
        self.crc = crc

    def value(self):
        # return ((self.crc & 0xff) << 8)|(self.crc & 0xff00) >> 8
        return self.crc

    def _update(self, crc: int, v: int):
        crc ^= v & 0xFF
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
        return crc
