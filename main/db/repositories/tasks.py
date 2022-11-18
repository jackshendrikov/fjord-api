from datetime import datetime
from typing import Any

from main.core.config import get_app_settings
from main.core.exceptions import TaskNotFoundException
from main.db.repositories.base import BaseMongoRepository
from main.schemas.tasks import TranslationTask

settings = get_app_settings()


class BaseTasksRepository(BaseMongoRepository):
    """
    Base repository to manipulate with the task Mongo collection.
    """

    def insert_translation_task(self, task: TranslationTask) -> None:
        """
        Insert translation task dict to MongoDB.
        """
        self.connection.insert_one(document=task.dict())

    def find_all_tasks(
        self, limit: int, offset: int
    ) -> tuple[int, list[TranslationTask]]:
        """
        Find first `limit` tasks skipping `offset` tasks.
        Return total amount of tasks and list with tasks which passes pagination condition.
        If any tasks no exist in DB return tuple with zero task number and empty tasks list.
        """
        total_queued_tasks = self.connection.count_documents(filter={})
        if total_queued_tasks:
            tasks = (
                self.connection.find()
                .sort(key_or_list="created_at", direction=1)
                .limit(limit)
                .skip(offset)
            )
            return total_queued_tasks, [TranslationTask(**task) for task in tasks]
        return 0, []

    def find_task_by_task_id(self, task_id: str) -> TranslationTask:
        """
        Return task by `task_id` field or rise an error if entity does not exists.
        """
        query = {"task_id": task_id}
        task = self.connection.find_one(filter=query)
        if not task:
            raise TaskNotFoundException(
                message=f"Task with id `{task_id}` not exists", status_code=404
            )
        return TranslationTask(**task)

    def get_tasks_with_state(self, state: str) -> list[TranslationTask]:
        """
        Find tasks with specific state.
        Return list of `TranslationTask` objects.
        """
        query = {"state": state}
        found_tasks = self.connection.find(filter=query)
        return [TranslationTask(**task) for task in found_tasks]

    def update_task_field(self, task_id: str, **values: Any) -> None:
        """Update specific task field with new value"""
        query = {"task_id": task_id}
        self.connection.update_one(
            filter=query, update={"$set": {**values, "updated_at": datetime.now()}}
        )


class TranslationTasksRepository(BaseTasksRepository):
    """
    Repository to manipulate with the regular crawling task Mongo collection.
    """

    db = settings.mongo_db
    collection = settings.mongo_tasks_collection
