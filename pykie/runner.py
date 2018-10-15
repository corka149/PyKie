from typing import List
from pykie.core import models

__author__ = "corka149"


import requests
from pykie.core import KieClient
from pykie.core.models import ProcessInstance


class ProcessLaunchError(Exception):
    pass


class ConditionalTaskVariables:

    def __init__(self, variables: dict, conditions: dict):
        self.variables = variables
        self.conditions = conditions

    def matches(self, task: models.Task):
        for tar_field, exp_value in self.conditions.items():
            for attr_name, attr_value in task.__dict__.items():
                if tar_field == attr_name and exp_value == attr_value:
                    return True
        return False


class MultiTaskVariables:

    def __init__(self):
        self.conditional_variables: List[ConditionalTaskVariables] = list()

    def add_conditional_variables(self, variables: dict, **conditions):
        self.conditional_variables.append(ConditionalTaskVariables(variables, conditions))

    def __iter__(self):
        for conditional_task_variable in self.conditional_variables:
            yield conditional_task_variable


class ProcessRunner:

    def __init__(self, kie_client: KieClient, container_id: str, process_definition_id: str):
        self.kie_client: KieClient = kie_client
        self.container_id: str = container_id
        self.process_def_id = process_definition_id
        self.process_instance: ProcessInstance = None

    def start(self, process_variables: dict):
        status_code, proc_id = self.kie_client.start_process(self.container_id, self.process_def_id, process_variables)
        if status_code == requests.codes.CREATED:
            self.process_instance = self.kie_client.get_process_instance(self.container_id, proc_id)
        else:
            raise ProcessLaunchError(f"It was not possible to launch process {self.process_def_id}.")

    def step(self, task_variables: dict):
        """Complete all tasks with the same variables."""
        tasks = self.kie_client.get_tasks_by_instance(self.process_instance.id)
        for task in tasks:
            self.kie_client.complete_task(self.container_id, task.id, task_variables)

    def step_different(self, task_variables: MultiTaskVariables):
        """Complete parallel active tasks with different variables."""
        pass

    def is_done(self)-> bool:
        """Returns true when process instance is finished"""
        tasks = self.kie_client.get_tasks_by_instance(self.process_instance.id)
        return len(tasks) == 0

    @staticmethod
    def __match_variables__(cond_variables, task: models.Task) -> dict:
        variables = dict()
        for cond_variable in cond_variables:
            if cond_variable.matches(task):
                variables.update(cond_variable.variables)
        return variables
