import pytest

from . import crc16


@pytest.mark.parametrize(
    "value, result",
    [
        (bytes.fromhex(""), 0xFFFF),
        # example from modbus website
        (bytes.fromhex("0207"), 0x1241),
        # instances from foxess bms/bat output.
        # note: crc is little endian in wire format.
        (bytes.fromhex("01 03 00 00 00 08 "), 0x0C44),
        (
            bytes.fromhex(
                "01 03 12 0c c2 0c c3 0c c1 0c c1 0c c0 0c c0 0c c0 00 00 00 00"
            ),
            0x04F1,
        ),
    ],
)
def test_crc16(value, result):
    crc = crc16.CRC16()
    crc.update_bytes(value)
    assert result == crc.value()
