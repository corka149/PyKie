import xml.etree.ElementTree as ET
import requests as r
import sys
import misc

base_url = "http://localhost:8080/kie-server/services/rest/server"

user = "kieserver"
password = "kieserver1!"
auth = (user, password)

container_results = r.get(base_url + "/containers", auth=auth)
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
