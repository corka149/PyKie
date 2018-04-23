__author__ = "corka149"

import xml.etree.ElementTree as ET
import requests as r
import misc

misc.print_banner()

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

    user = "kieserver"
    password = "kieserver1!"
    auth = (user, password)

    container_results = r.get(container_url, auth=auth)
    root = ET.fromstring(container_results.text)

    container_ids = list()
    for container in root.iter("kie-container"):
        container_ids.append(container.attrib["container-id"])

    selected = ""
    should_quit = False
    while not should_quit:
        print("\nSelect one [q for quit]")
        for key, val in enumerate(container_ids):
            print("{}: {}".format(key, val))
        selected = input("Choose one: ")

        if selected.isdigit() and 0 <= int(selected) < len(container_ids):
            should_quit = True
        elif selected == "q":
            should_quit = True

    if selected != "q":
        selected_container = container_ids[int(selected)]
        definitions_result = r.get(instance_url.format(selected_container) + "?page=0&pageSize=100&sortOrder=true",
                                   auth=auth)
        instances = ET.fromstringlist(definitions_result.text)
        for instance in instances.iter("process-instance"):
            delete_url = instance_url.format(selected_container) + "/" + instance.find("process-instance-id").text
            delete_result = r.delete(delete_url, auth=auth)
            if delete_result.status_code == 204:
                print("Delete process instance {} - {}".format(instance.find("process-instance-id").text,
                                                               instance.find("process-name").text))

        container_results = r.delete(container_url + "/" + selected_container, auth=auth)
        if container_results.status_code == 200:
            print("Successfully disposed container {}".format(selected_container))
        else:
            print("Disposing of container {} failed.".format(selected_container))
