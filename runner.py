__author__ = "corka149"

from core import KieClient
from core.models import ProcessInstance


class ProcessRunner:

    def __init__(self, kie_client: KieClient, container_id: str, process_definition_id: str):
        self.kie_client: KieClient = kie_client
        self.container_id: str = container_id
        self.process_def_id = process_definition_id
        self.process_instance: ProcessInstance = None

    def start(self, process_variables: dict):
        self.process_instance = self.kie_client.start_process(self.container_id, self.process_def_id, process_variables)

    def step(self, task_variables: dict):
        """Complete all tasks with the same variables."""
        tasks = self.kie_client.get_tasks_by_instance(self.process_instance.id)
        for task in tasks:
            self.kie_client.complete_task(self.container_id, task.id, task_variables)

    def step_different(self):
        """Complete parallel active tasks with different variables."""
        pass


class MultiTaskVariables:

    def __init__(self):
        pass
