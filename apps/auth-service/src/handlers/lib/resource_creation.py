import json
import re

class Policy:

    def __init__(self, resource_endpoint, action, action_name):
        self.resource_endpoint = resource_endpoint
        self.action = action
        self.action_name = action_name

    def __repr__(self):
        return f"""permit(
    principal,
    action == Action::\"{self.action}\",
    resource == Api::\"{self.resource_endpoint}\"
);

    """


def get_all_policies(json_text):
    def __traverse_items(items, policies=[]):
        for i in items:
            request = i.get("request")
            if not request is None:
                action = request["method"]
                url_path = request["url"]["path"]
                slug_pattern_1 = r"\{[a-zA-Z_]+[a-zA-Z0-9_]+\}"
                slug_pattern_2 = r":[a-zA-Z_]+[a-zA-Z0-9_]+"
                url = ""
                for url_part in url_path:
                    if re.match(slug_pattern_1, url_part) or re.match(slug_pattern_2, url_part):
                        url += "/*"
                    else:
                        url += f"/{url_part}"
                policy = Policy(resource_endpoint=url, action=action, action_name=i["name"])
                policies.append(policy)
            next_item = i.get("item")
            if not next_item is None:
                __traverse_items(next_item, policies)

    map = json.loads(json_text)
    policies = []
    __traverse_items(map["item"], policies)
    return policies

# def test_get_all_resources():
#     with open("cedar_test_resources.json", "r") as file:
#         json_text = file.read()

#     policies = get_all_policies(json_text)
#     for policy in policies:
#         print(policy.action_name)
