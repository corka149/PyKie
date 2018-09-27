from . import kie_bindings
from . import models
import requests


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

    def __get__(self, url):
        return requests.get(url, auth=self.__auth__, headers=self.__headers)
