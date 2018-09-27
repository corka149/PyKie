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

    def __get__(self, url):
        return requests.get(url, auth=self.__auth__, headers=self.__headers)
