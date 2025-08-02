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


def get_next_rotation(file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["next_rotation"]


def update_next_rotation(new_rotation, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["next_rotation"] = new_rotation

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_all_permissions(file_path: str = "database/data.json") -> list:
    with open(file_path, "r") as f:
        data = json.load(f)

    return data.get("permissions", [])


def get_permission(user_id: str, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        for entry in data.get("permissions", []):
            if user_id in entry:
                return entry[user_id]

    return False


def add_permission(user_id: str, role: str, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])

        for entry in permissions:
            if user_id in entry:
                raise ValueError("User already exists")

        permissions.append({user_id: role})
        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def update_permission(
    user_id: str, new_role: str, file_path: str = "database/data.json"
):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])

        for entry in permissions:
            if user_id in entry:
                entry[user_id] = new_role
                break
        else:
            raise ValueError("User not found")

        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def remove_permission(user_id: str, file_path: str = "database/data.json"):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])
        permissions = [entry for entry in permissions if user_id not in entry]
        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
