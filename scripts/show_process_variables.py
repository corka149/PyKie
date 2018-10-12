__author__ = "corka149"

from pykie.core import KieClient
import logging as log
from pykie import misc


def main():
    misc.print_banner()

    kie_servers = ["127.0.0.1:8180"]
    kie_server = misc.force_to_input(kie_servers)

    if kie_server is not None:
        protocol = "http"
        if "https" in kie_server:
            protocol = "https"
        if "http" in kie_server or "https" in kie_server:
            kie_server = kie_server.split("//")[1]

        auth = misc.request_credentials()
        kc = KieClient(kie_server, auth, protocol)

        containers = kc.get_containers()
        container_ids = [container.container_id for container in containers]
        selected_container = misc.force_to_input(container_ids)

        if selected_container is not None:
            instances = kc.get_process_instances(selected_container)
            process_id = misc.force_to_input(
                [instance.id for instance in instances])

            if process_id is not None:
                variables = kc.get_process_variables(
                    selected_container, process_id)
                for k, v in variables.items():
                    print(f"key: {k} - value: {v}")

    input("Request done [Press any key]")


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
