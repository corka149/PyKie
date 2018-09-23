
base_url = "http://{kie_server}kie-server/services/rest/server"


def containers(kie_server):
    return base_url.format(kie_server=kie_server) + "/containers"


def process_instances(kie_server, container_id):
    return containers(kie_server) + f"/{container_id}"


def process_instances_variables(kie_server, container_id, process_id):
    return process_instances(kie_server, container_id) + f"/processes/instances/{process_id}/variables"


def process_instance(kie_server, container_id, process_id, with_vars):
    vars_requested = ""
    if with_vars:
        vars_requested = "?withVars={with_vars}"
    return process_instances(kie_server, container_id) + f"/processes/instances/{process_id}" + vars_requested
