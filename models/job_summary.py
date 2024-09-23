from dataclasses import dataclass
from typing import List


@dataclass()
class JobSummary:
    id: str = ""
    name: str = ""
    url: str = ""
    company: str = ""
    area: str = ""
    tags: List[str] = None
    salary: str = ""
    language: str = ""
