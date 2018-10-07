from datetime import datetime


class KieContainer:

    def __init__(self, json):
        self.container_id = json.get("container-id")
        self.release_id = json.get("resolved-release-id")
        self.status = json.get("status")
        self.config_items = json.get("config-items")
        self.messages = json.get("messages")
        self.container_alias = json.get("container-alias")


class ProcessInstance:

    def __init__(self, json):
        self.id = json.get("process-instance-id")
        self.definition_id = json.get("process-id")
        self.definition_name = json.get("process-name")
        self.version = json.get("process-version")
        self.instance_state = json.get("process-instance-state")
        self.start_date = datetime.fromtimestamp(json.get("start-date").get("java.util.Date") / 1000)


class Task:

    def __init__(self, json):
        self.id = json.get("task-id")
        self.name = json.get("task-name")
        self.description = json.get("task-description")
        self.actual_owner = json.get("task-actual-owner")
        self.created_on = datetime.fromtimestamp(json.get("task-created-on").get("java.util.Date") / 1000)
        self.container_id = json.get("task-container-id")
        self.proc_inst_id = json.get("task-proc-inst-id")
        self.proc_def_id = json.get("task-proc-def-id")
        self.status = json.get("task-status")