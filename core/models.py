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
