def find_by_id(collection, id):
    id = int(id)
    for c in collection:
        c_id = c.get("id")
        if c_id is None: continue
        elif c_id == id: return c
