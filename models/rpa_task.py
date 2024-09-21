from dataclasses import dataclass

from models.task_status import TaskStatus


@dataclass(init=False)
class RpaTask:
    action: str
    data: str
    id: str
    retry: int
    status: TaskStatus
