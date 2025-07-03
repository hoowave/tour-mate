from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CsvDto:
    addr1: str                  # 추천 목적지
    addr2: str                  # 추천 목적지 시  
    addr3: Optional[str]        # 추천 목적지 구

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            addr1=data.get("addr1", ""),
            addr2=data.get("addr2", ""),
            addr3=data.get("addr3")
        )
    
    @staticmethod
    def get_sample_data() -> List['CsvDto']:
        return [
            CsvDto(addr1="광안리 해수욕장", addr2="부산", addr3="수영구"),
            CsvDto(addr1="해운대 해수욕장", addr2="부산", addr3="해운대구"),
            CsvDto(addr1="경복궁", addr2="서울", addr3="종로구"),
            CsvDto(addr1="남산타워", addr2="서울", addr3="용산구"),
            CsvDto(addr1="정동진 해변", addr2="강원특별자치도", addr3="강릉시")
        ]