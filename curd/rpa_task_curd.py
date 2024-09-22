from sqlalchemy.orm import Session

from database.database import get_db
from models.rpa_task import RpaTask
from models.task_status import TaskStatus
from schemas.rpa_task_schema import RpaTask as RpaTaskSchema


def get_rpa_task(
    action=None, data=None, id=None, db: Session = next(get_db())
) -> RpaTaskSchema:
    if action and data:
        exist = (
            db.query(RpaTaskSchema)
            .filter(RpaTaskSchema.action == action, RpaTaskSchema.data == data)
            .first()
        )
        if exist:
            return exist
        return None
    elif id:
        return db.query(RpaTaskSchema).filter(RpaTaskSchema.id == id).first()
    else:
        raise ValueError("Invalid arguments for get_rpa_task")


def create_rpa_task(rpa_task: RpaTask, db: Session = next(get_db())) -> RpaTaskSchema:
    rpa_task_schema = RpaTaskSchema()
    rpa_task_schema.action = rpa_task.action
    rpa_task_schema.data = rpa_task.data
    rpa_task_schema.id = rpa_task.id
    db.add(rpa_task_schema)
    db.commit()
    db.refresh(rpa_task_schema)
    return rpa_task_schema


def update_rpa_task_status(
    task_id: str, status: TaskStatus, db: Session = next(get_db())
) -> RpaTaskSchema:
    rpa_task_schema = get_rpa_task(id=task_id, db=db)
    if rpa_task_schema is None:
        return None
    rpa_task_schema.status = status
    db.commit()
    db.refresh(rpa_task_schema)
    return rpa_task_schema
