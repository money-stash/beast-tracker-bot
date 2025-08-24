import json
from config import ADMIN_ID, DATA_JSON


def get_group_id(file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["group_id"]


def update_group_id(new_group_id, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["group_id"] = new_group_id

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_rot_freq(file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["partner_rot_freq"]


def update_rot_freq(new_freq, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["partner_rot_freq"] = new_freq

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_dme_hours(file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["dme_hours"]


def update_dme_hours(new_hours, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["dme_hours"] = new_hours

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_next_rotation(file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data["next_rotation"]


def update_next_rotation(new_rotation, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)

    data["next_rotation"] = new_rotation

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_all_permissions(file_path: str = DATA_JSON) -> list:
    with open(file_path, "r") as f:
        data = json.load(f)

    return data.get("permissions", [])


def get_permission(user_id: str, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        for entry in data.get("permissions", []):
            if str(user_id) in entry:
                return entry[str(user_id)]
    return False


def add_permission(user_id: str, role: str, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])

        for entry in permissions:
            if str(user_id) in entry:
                raise ValueError("User already exists")

        permissions.append({str(user_id): role})
        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def update_permission(user_id: str, new_role: str, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])

        for entry in permissions:
            if str(user_id) in entry:
                entry[str(user_id)] = new_role
                break
        else:
            raise ValueError("User not found")

        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def remove_permission(user_id: str, file_path: str = DATA_JSON):
    with open(file_path, "r") as f:
        data = json.load(f)
        permissions = data.get("permissions", [])
        permissions = [entry for entry in permissions if str(user_id) not in entry]
        data["permissions"] = permissions

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_admins() -> list[int]:
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_admins = []
    for perm in data.get("permissions", []):
        for uid, role in perm.items():
            if role == "admin":
                file_admins.append(int(uid))

    return list(set(ADMIN_ID + file_admins))


def get_schedulers() -> list[int]:
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    schedulers = []
    for perm in data.get("permissions", []):
        for uid, role in perm.items():
            if role == "scheduler":
                schedulers.append(int(uid))

    return schedulers
