__author__ = "corka149"

from pprint import pprint
from core import KieClient
import concurrent.futures
import xml.etree.ElementTree as ET
import requests as r
import misc
import time


def main():
    misc.print_banner()

    kie_servers = ["127.0.0.1:8180"]
    kie_server = misc.force_to_input(kie_servers)

    if kie_server is not None:
        auth = misc.request_credentials()
        kc = KieClient(kie_server, auth)
        base_url = "http://" + kie_server + "/kie-server/services/rest/server"
        container_url = base_url + "/containers"
        process_url = container_url + "/{}/processes"
        instance_url = process_url + "/instances"

        containers = kc.request_containers()
        container_ids = [container.container_id for container in containers]
        selected_container = misc.force_to_input(container_ids)

        if selected_container is not None:
            definitions_result = r.get(instance_url.format(selected_container) + "?page=0&pageSize=100&sortOrder=true",
                                       auth=auth)
            instances = ET.fromstringlist(definitions_result.text)
            to_delete = list()
            start = time.time()
            for instance in instances.iter("process-instance"):
                to_delete.append(instance_url.format(selected_container) + "/" + instance.find("process-instance-id").text)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = tuple(executor.map(lambda url: r.delete(url, auth=auth), to_delete))
                print("Amount of delete-requests: {}".format(len(result)))
                pprint(result)

            container_results = r.delete(container_url + "/" + selected_container, auth=auth)
            print("Delete-request for container {} ends with {}.".format(selected_container, container_results.status_code))
            print(f'\nTime to complete {time.time() - start:.2f}s\n')

    input("Request done [Press any key]")


if __name__ == '__main__':
    main()
