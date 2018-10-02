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
        self.process_instance_id = json.get("process-instance-id")
        self.process_id = json.get("process-id")
        self.process_name = json.get("process-name")
        self.process_version = json.get("process-version")
        self.process_instance_state = json.get("process-instance-state")
        self.start_date = datetime.fromtimestamp(json.get("start-date").get("java.util.Date") / 1000)


class Task:

    def __init__(self, json):
        self.task_id = json.get("task-id")
        self.task_name = json.get("task-name")
        self.task_description = json.get("task-description")
        self.task_actual_owner = json.get("task-actual-owner")
        self.task_created_on = datetime.fromtimestamp(json.get("task-created-on").get("java.util.Date") / 1000)
        self.task_container_id = json.get("task-container-id")
        self.task_proc_inst_id = json.get("task-proc-inst-id")
        self.task_proc_def_id = json.get("task-proc-def-id")
