from enum import Enum


class TaskStatus(Enum):
    PENDING = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4
