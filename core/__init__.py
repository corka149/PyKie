from . import kie_bindings
from . import models
import requests
import logging


class KieClient:

    def __init__(self, kie_server, auth):
        self.__kie_server__ = kie_server
        self.__auth__ = auth
        self.__headers = {"accept": "application/json"}

    def request_containers(self):
        containers_url = kie_bindings.containers(self.__kie_server__)
        container_results = self.__get__(containers_url)
        containers = container_results.json().get("result").get("kie-containers").get("kie-container")
        return [models.KieContainer(container) for container in containers]

    def request_process_instances(self, container_id):
        instances_url = kie_bindings.process_instances(self.__kie_server__, container_id)
        instances_result = self.__get__(instances_url)
        instances = instances_result.json().get("process-instance")
        return [models.ProcessInstance(instance) for instance in instances]

    def request_process_variables(self, container_id, process_instance_id):
        url = kie_bindings.process_instances_variables(self.__kie_server__, container_id, process_instance_id)
        variables_result = self.__get__(url)
        return variables_result.json()

    def delete_container(self, container_id):
        url = kie_bindings.containers(container_id) + f"/{container_id}"
        return self.__delete__(url).status_code

    def delete_process_instance(self, container_id, process_instance_id):
        url = kie_bindings.process_instances(self.__kie_server__, container_id) + f"/{process_instance_id}"
        return self.__delete__(url).status_code

    def __get__(self, url):
        logging.debug(f"GET - {url}")
        return requests.get(url, auth=self.__auth__, headers=self.__headers)

    def __delete__(self, url):
        logging.debug(f"DELETE - {url}")
        return requests.delete(url, auth=self.__auth__)
