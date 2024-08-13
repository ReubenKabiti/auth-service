import json

def get_all_resources(json_text):
    def __helper(items, parent=None):

        paths = []

        if items is None:
            return parent

        for item in items:
            new_items = item.get("item")
            item_name = item.get("name")
            new_parent_name = None
            if parent is None:
                new_parent_name = item_name
            else:
                new_parent_name = f"{parent}::\"{item_name}\""
            out = __helper(new_items, new_parent_name)
            paths.append(out)
        return paths

    map = json.loads(json_text)
    items = map.get("item")
    return __helper(items)


def test_get_all_resources():
    with open("cedar_test_resources.json", "r") as file:
        json_text = file.read()
    res = get_all_resources(json_text)
    print(res)
