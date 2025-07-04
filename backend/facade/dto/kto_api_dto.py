from dataclasses import dataclass
from typing import Optional

@dataclass
class KtoApiDto:
    addr1: str
    firstimage: Optional[str]
    title: str
    tel: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            addr1 = data.get("addr1", ""),
            firstimage = data.get("firstimage"),
            title = data.get("title", ""),
            tel = data.get("tel")
        )