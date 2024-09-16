from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(init=False)
class JobSummary:
    id: str = ""
    name: str = ""
    url: str = ""
    company: str = ""
    area: str = ""
    tags: List[str] = None
    salary: str = ""
    language: str = ""
