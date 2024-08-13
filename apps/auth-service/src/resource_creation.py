import json

class Resource:
    def __init__(self, name, request):
        self.name = name
        self.request = request

    def __repr__(self):
        return f"{self.name} -- {self.request}"

def get_all_resources(json_text):
    def __helper(items, parent=None, request=None):

        paths = []

        if items is None:
            return Resource(name=parent, request=request)

        for item in items:
            new_items = item.get("item")
            item_name = item.get("name")
            request = item.get("request")
            new_parent_name = None
            if parent is None:
                new_parent_name = item_name
            else:
                new_parent_name = f"{parent}::\"{item_name}\""
            out = __helper(items=new_items, parent=new_parent_name, request=request)
            if type(out) is Resource:
                paths.append(out)
            else:
                paths.extend(out)
        return paths


    map = json.loads(json_text)
    items = map.get("item")
    res = __helper(items)
    return res


def test_get_all_resources():
    with open("cedar_test_resources.json", "r") as file:
        json_text = file.read()

    res = get_all_resources(json_text)
    print(res)
