import dataclasses
import typing

RegisterID = int
RegisterValue = int


@dataclasses.dataclass
class MasterReadRegMulti:
    begin: RegisterID
    len: int


@dataclasses.dataclass
class SlaveReadRegMulti:
    values: typing.List[RegisterValue]


MasterPDU = typing.Union[MasterReadRegMulti]

SlavePDU = typing.Union[SlaveReadRegMulti]
