import json
import re

class ResourceAction:
    """
    Class for storing actions and the resource they affects
    """
    def __init__(self, name, request):
        self.name = name
        self.request = request
        self.action = self.get_action()
        self.regex = self.get_regex()

    def __repr__(self):
        o = f"{self.name}\n"
        o += f"{self.get_url()}\n"
        o += f"{self.get_action()}\n"
        return o

    def get_url(self):
        url_parts = self.request["url"]["path"]
        slug_pattern_1 = r"\{[a-zA-Z_]+[a-zA-Z_0-9]\}"
        slug_pattern_2 = r"^:[a-zA-Z_]+[a-zA-Z_0-9]"

        for i, part in enumerate(url_parts):
            if re.match(slug_pattern_1, part) or re.match(slug_pattern_2, part):
                url_parts[i] = "*"

        return "/".join(url_parts)


    def get_action(self):
        return f'Action::"{self.request.get("method")}"'

    def get_policy_name(self):
        return self.name.split("::")[-1].replace('"', "")

    def get_regex(self):
        url = self.get_url()
        slug_pattern = r"[0-9a-zA-Z_]"
        url = url.replace("*", slug_pattern)
        url = f"/?{url}/?"
        return url

def get_all_resources(json_text):
    def __helper(items, parent=None, request=None):

        paths = []

        if items is None:
            return ResourceAction(name=parent, request=request)

        for item in items:
            new_items = item.get("item")
            item_name = item.get("name").replace(" ", "")
            request = item.get("request")
            new_parent_name = None
            if parent is None:
                new_parent_name = item_name
            else:
                new_parent_name = f"{parent}::\"{item_name}\""
            out = __helper(items=new_items, parent=new_parent_name, request=request)
            if type(out) is ResourceAction:
                paths.append(out)
            else:
                paths.extend(out)
        return paths


    map = json.loads(json_text)
    items = map.get("item")
    res = __helper(items)
    return res

def create_policy(resource_action):
    return f"""permit(
    principal,
    action == { resource_action.get_action() },
    resource == { resource_action.name }
);
        """

# def generate_policies(json_text):
#     resources = get_all_resources(json_text)
#     for resource in resources:

def test_get_all_resources():
    with open("cedar_test_resources.json", "r") as file:
        json_text = file.read()

    res = get_all_resources(json_text)
    for r in res:
        print(create_policy(r))
        # print(f"{r.get_url()} -- {r.get_action()}")
        # print(r.get_regex())
