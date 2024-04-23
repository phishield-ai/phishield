from enum import Enum

from dramatiq import Broker, Message, Middleware
from dramatiq.results.backends import RedisBackend


class TaskStatus(Enum):
    """
    Represents the status of a task in a distributed task system.

    Attributes:
    - QUEUED:       The initial status after task creation.
                    Indicates that the task is waiting in the queue to be processed.
                    This status is automatically assigned when the task is registered with the task management system.
    - IN_PROGRESS:  Indicates that the task is currently being executed.
                    This status is set after the task system acknowledges the task's commencement.
    - SUCCESS:      Marks the successful completion of a task.
                    This status is assigned when the task finishes its execution without any errors or interruptions.
    - FAILED:       Represents a task that has ended with errors.
                    This status is used when the task cannot be completed successfully due to exceptions or runtime errors.
    - DEFERRED:     Indicates a task that has been postponed for later execution.
                    This status is used for tasks that are not executed immediately upon queuing, either due to:
                        1. specific scheduling requirements
                        2. system-defined criteria
                        3. errors found during execution
    """

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    DEFERRED = "deferred"


class Status(Middleware):
    backend: RedisBackend

    def __init__(self, backend: RedisBackend):
        self.backend = backend

    def _set_status(self, message: Message, status: TaskStatus):
        self.backend.client.set(message.message_id, status.value)

    def _get_status(self, message: Message):
        return self.backend.client.get(message.message_id)

    def before_enqueue(self, broker: Broker, message: Message, delay):
        status = self._get_status(message)

        # Only set to QUEUED the first time
        # (Retry middleware enqueues on each retry)
        if not status:
            self._set_status(message, TaskStatus.QUEUED)

    def before_process_message(self, broker: Broker, message: Message):
        self._set_status(message, TaskStatus.IN_PROGRESS)

    def after_process_message(self, broker: Broker, message: Message, *, result=None, exception=None):
        # NOTE: This should be implemented after Retries middleware is fixed
        #
        # if message.failed:
        #     self._set_status(message, TaskStatus.FAILED)
        #     return

        if not exception:
            self._set_status(message, TaskStatus.SUCCESS)
            return

        actor = broker.get_actor(message.actor_name)
        retries = message.options.get("retries", 0)
        max_retries = message.options.get("max_retries") or actor.options.get("max_retries", 0)

        if retries < max_retries:
            self._set_status(message, TaskStatus.DEFERRED)
        else:
            self._set_status(message, TaskStatus.FAILED)
