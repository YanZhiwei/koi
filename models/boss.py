from dataclasses import dataclass


@dataclass(init=False)
class Boss:
    name: str = ""
    title: str = ""
    active_state: str = ""
