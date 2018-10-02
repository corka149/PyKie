__author__ = "corka149"

from core import KieClient
import logging as log
import misc


def main():
    misc.print_banner()

    kie_servers = ["127.0.0.1:8180"]
    kie_server = misc.force_to_input(kie_servers)

    if kie_server is not None:
        auth = misc.request_credentials()
        kc = KieClient(kie_server, auth)

        containers = kc.request_containers()
        container_ids = [container.container_id for container in containers]
        selected_container = misc.force_to_input(container_ids)

        if selected_container is not None:
            instances = kc.request_process_instances(selected_container)
            process_id = misc.force_to_input([instance.process_instance_id for instance in instances])

            if process_id is not None:
                variables = kc.request_process_variables(selected_container, process_id)
                for k, v in variables.items():
                    print(f"key: {k} - value: {v}")

    input("Request done [Press any key]")


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
