__author__ = "corka149"

from core import KieClient
import xml.etree.ElementTree as ET
import requests as r
import misc


def main():
    misc.print_banner()

    kie_servers = ["127.0.0.1:8180"]
    kie_server = misc.force_to_input(kie_servers)

    if kie_server is not None:
        auth = misc.request_credentials()
        kc = KieClient(kie_server, auth)
        base_url = "http://" + kie_server + "/kie-server/services/rest/server"

        containers = kc.request_containers()
        container_ids = [container.container_id for container in containers]
        selected_container = misc.force_to_input(container_ids)

        if selected_container is not None:
            instances = kc.request_process_instances(selected_container)
            process_id = misc.force_to_input([instance.process_instance_id for instance in instances])

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
