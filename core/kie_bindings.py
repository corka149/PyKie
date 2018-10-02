
base_url = "http://{kie_server}/kie-server/services/rest/server"


def containers(kie_server):
    return base_url.format(kie_server=kie_server) + "/containers"


def process_definition_instances(kie_server, container_id, process_definition_id):
    return containers(kie_server) + f"/{container_id}/processes/{process_definition_id}/instances"


def process_instances(kie_server, container_id):
    return containers(kie_server) + f"/{container_id}/processes/instances"


def process_instances_variables(kie_server, container_id, process_id):
    return process_instances(kie_server, container_id) + f"/{process_id}/variables"


def process_instance(kie_server, container_id, process_id, with_vars):
    vars_requested = ""
    if with_vars:
        vars_requested = "?withVars={with_vars}"
    return process_instances(kie_server, container_id) + f"/{process_id}" + vars_requested


def task_query(kie_server, process_id):
    return base_url.format(kie_server=kie_server) + f"/queries/tasks/instances/process/{process_id}"
