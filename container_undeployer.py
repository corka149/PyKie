__author__ = "corka149"

from core import KieClient
import logging as log
import concurrent.futures
import misc


def main():
    misc.print_banner()

    kie_servers = ["127.0.0.1:8180"]
    kie_server = misc.force_to_input(kie_servers)

    if kie_server is not None:
        auth = misc.request_credentials()
        kc = KieClient(kie_server, auth)

        containers = kc.get_containers()
        container_ids = [container.container_id for container in containers]
        container_id = misc.force_to_input(container_ids)

        if container_id is not None:
            process_instances = kc.get_process_instances(container_id)

            def delete_instance(instance):
                return kc.delete_process_instance(container_id, instance.process_instance_id)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = tuple(executor.map(delete_instance, process_instances))
                log.info(str(result))

            status_code = kc.delete_container(container_id)
            log.info("Delete-request for container {} ends with {}.".format(container_id, status_code))

    input("Request done [Press any key]")


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
