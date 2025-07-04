from dataclasses import dataclass

@dataclass
class WebSearchDto:
    location: str
    info: str
    url: str