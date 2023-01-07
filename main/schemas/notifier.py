from pydantic import BaseModel


class NotifierError(BaseModel):
    task_id: str
    error_msg: str
