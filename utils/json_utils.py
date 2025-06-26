import json


def get_group_id(file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["group_id"]


def update_group_id(new_group_id, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["group_id"] = new_group_id

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
