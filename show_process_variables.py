__author__ = "corka149"

from getpass import getpass
from pprint import pprint
import concurrent.futures
import xml.etree.ElementTree as ET
import requests as r
import misc
import time

misc.print_banner()

kie_servers = ["127.0.0.1:8080"]
selected = ""

while not (selected.isdigit() and 0 <= int(selected) < len(kie_servers)) and selected != "q":
	print("Select one [q for quit]:")
	for k, v in enumerate(kie_servers):
		print("{}: {}".format(k, v))
	selected = input("Choose one: ")

if selected != "q":
	auth = ("kieserver", "kieserver1!")
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
		process_ids = list()
		start = time.time()
		for instance in instances.iter("process-instance"):
			process_ids.append(instance.find("process-instance-id").text)

		print(f"process_ids {process_ids}")
		selected = ""
		while not (selected.isdigit() and 0 <= int(selected) < len(process_ids)) and selected != "q":
			print("\nSelect one [q for quit]")
			for key, val in enumerate(process_ids):
				print("{}: {}".format(key, val))
			selected = input("Choose one: ")
		if selected != "q":
			variables_resp = r.get(f"{base_url}/containers/{selected_container}/processes/instances/{process_ids[int(selected)]}/variables/instances", auth=auth)
			variables = ET.fromstringlist(variables_resp.text)
			variables = [(var.find("name").text, var.find("value").text) for var in variables]
			for var in variables:
				print(f"\t{var[0]} : {var[1]}")
input("Request done [Press any key]")
