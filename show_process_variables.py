__author__ = "corka149"

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
        base_url = "http://" + kie_server + "/kie-server/services/rest/server"
        container_url = base_url + "/containers"
        process_url = container_url + "/{}/processes"
        instance_url = process_url + "/instances"

        container_results = r.get(container_url, auth=auth)
        root = ET.fromstring(container_results.text)

        container_ids = [container.attrib["container-id"] for container in root.iter("kie-container")]
        selected_container = misc.force_to_input(container_ids)

        if selected_container is not None:
            definitions_result = r.get(instance_url.format(selected_container) + "?page=0&pageSize=100&sortOrder=true",
                                       auth=auth)
            instances = ET.fromstringlist(definitions_result.text)
            process_ids = list()
            start = time.time()
            for instance in instances.iter("process-instance"):
                process_ids.append(instance.find("process-instance-id").text)

            process_id = misc.force_to_input(process_ids)
            if process_id is not None:
                variables_resp = r.get(
                    f"{base_url}/containers/{selected_container}/processes/instances/{process_id}/variables/instances",
                    auth=auth)
                variables = ET.fromstringlist(variables_resp.text)
                variables = [(var.find("name").text, var.find("value").text) for var in variables]
                for var in variables:
                    print(f"\t{var[0]} : {var[1]}")
    input("Request done [Press any key]")


if __name__ == '__main__':
    main()
