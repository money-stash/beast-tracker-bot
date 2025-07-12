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


def get_rot_freq(file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["partner_rot_freq"]


def update_rot_freq(new_freq, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["partner_rot_freq"] = new_freq

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_dme_hours(file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["dme_hours"]


def update_dme_hours(new_hours, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["dme_hours"] = new_hours

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
