__author__ = "corka149"

from pprint import pprint
import concurrent.futures
import xml.etree.ElementTree as ET
import requests as r
import misc
import time

misc.print_banner()

auth = ("kieserver", "kieserver1!")
kie_servers = ["localhost:8080"]
selected = ""

while not (selected.isdigit() and 0 <= int(selected) < len(kie_servers)) and selected != "q":
    print("Select one [q for quit]:")
    for k, v in enumerate(kie_servers):
        print("{}: {}".format(k, v))
    selected = input("Choose one: ")

if selected != "q":
    base_url = "http://" + kie_servers[int(selected)] + "/kie-server/services/rest/server"
    container_url = base_url + "/containers"
    process_url = container_url + "/{}/processes"
    instance_url = process_url + "/instances"

    container_results = r.get(container_url, auth=auth)
    root = ET.fromstring(container_results.text)

    container_ids = [container.attrib["container-id"] for container in root.iter("kie-container")]

    selected = ""
    while not (selected.isdigit() and 0 <= int(selected) < len(container_ids)) and selected != "q":
        print("\nSelect one [q for quit]")
        for key, val in enumerate(container_ids):
            print("{}: {}".format(key, val))
        selected = input("Choose one: ")

    if selected != "q":
        selected_container = container_ids[int(selected)]
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
