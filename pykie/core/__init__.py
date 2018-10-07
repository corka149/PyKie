from requests import RequestException

from . import kie_bindings
from . import models
import requests
import logging


class KieServerUnavailableError(Exception):
    pass


class KieClient:

    def __init__(self, kie_server, auth, protocol="http"):
        self.__kie_server__ = protocol + "://" + kie_server
        self.__auth__ = auth
        self.__headers__ = {"accept": "application/json", "content-type": "application/json"}
        try:
            url = kie_bindings.kie_readycheck(self.__kie_server__)
            resp = requests.get(url, auth=self.__auth__)
            if resp.status_code != requests.codes.OK:
                raise KieServerUnavailableError(f"{kie_server} is not ready yet.")
        except RequestException:
            raise KieServerUnavailableError(f"{kie_server} does not answer.")

    def get_containers(self):
        containers_url = kie_bindings.containers(self.__kie_server__)
        container_results = self.__request_get__(containers_url)
        containers = container_results.json().get("result").get("kie-containers").get("kie-container")
        return [models.KieContainer(container) for container in containers]

    def get_process_instances(self, container_id: str):
        instances_url = kie_bindings.process_instances(self.__kie_server__, container_id)
        instances_result = self.__request_get__(instances_url)
        instances = instances_result.json().get("process-instance")
        return [models.ProcessInstance(instance) for instance in instances]

    def get_process_instance(self, container_id: str, process_id:str ):
        instance_url = kie_bindings.process_instance(self.__kie_server__, container_id, process_id, False)
        instance_result = self.__request_get__(instance_url)
        return models.ProcessInstance(instance_result.json())

    def get_process_variables(self, container_id: str, process_instance_id: str):
        url = kie_bindings.process_instances_variables(self.__kie_server__, container_id, process_instance_id)
        variables_result = self.__request_get__(url)
        return variables_result.json()

    def delete_container(self, container_id: str):
        url = kie_bindings.containers(container_id) + f"/{container_id}"
        return self.__request_delete__(url).status_code

    def delete_process_instance(self, container_id: str, process_instance_id: str):
        url = kie_bindings.process_instances(self.__kie_server__, container_id) + f"/{process_instance_id}"
        return self.__request_delete__(url).status_code

    def start_process(self, container_id: str, process_definition_id: str, variable_dict=None):
        """Starts a new process instance. It will return the status code of the request and the process id."""
        if variable_dict is None:
            variable_dict = dict()
        url = kie_bindings.process_definition_instances(self.__kie_server__, container_id, process_definition_id)
        resp = self.__request_post__(url, variable_dict)
        return resp.status_code, resp.json()

    def get_tasks_by_instance(self, process_instance_id: str):
        url = kie_bindings.task_query(self.__kie_server__, process_instance_id)
        resp = self.__request_get__(url)
        return [models.Task(json) for json in resp.json().get("task-summary")]

    def complete_task(self, container_id: str, task_id: str, variable_dict=None):
        """Completes a task and return the response status code."""
        if variable_dict is None:
            variable_dict = dict()
        url = kie_bindings.task_state_complete(self.__kie_server__, container_id, task_id)
        return self.__request_put__(url, variable_dict).status_code

    def __request_get__(self, url: str):
        logging.debug(f"GET - {url}")
        return requests.get(url, auth=self.__auth__, headers=self.__headers__)

    def __request_delete__(self, url: str):
        logging.debug(f"DELETE - {url}")
        return requests.delete(url, auth=self.__auth__)

    def __request_post__(self, url: str, data: dict):
        logging.debug(f"POST - {url} - Body: {data}")
        return requests.post(url, json=data, auth=self.__auth__, headers=self.__headers__)

    def __request_put__(self, url: str, data: dict):
        logging.debug(f"PUT- {url} - Body: {data}")
        return requests.put(url, json=data, auth=self.__auth__, headers=self.__headers__)
