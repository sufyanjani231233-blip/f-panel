import json
from datetime import datetime

FILE = "users.json"

today = datetime.utcnow().date()
changed = False

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


for owner_name, owner in data.items():

    if not isinstance(owner, dict):
        continue

    for username, user in owner.items():

        if not isinstance(user, dict):
            continue

        # Skip free users only
        if user.get("isFreeUser", False):
            continue

        hwid = str(user.get("hwid", "")).strip()
        reset_date = str(user.get("hwid_reset_date", "")).strip()

        # Nothing to reset
        if hwid == "" or reset_date == "":
            continue

        try:

            reset = datetime.strptime(reset_date, "%Y-%m-%d").date()

            if today >= reset:

                user["hwid"] = ""
                user["hwid_bind_date"] = ""
                user["hwid_reset_date"] = ""
                user["last_reset_date"] = today.strftime("%Y-%m-%d")

                changed = True

                print(f"[RESET] {owner_name} -> {username}")

        except Exception as e:

            print(f"[SKIP] {username}: {e}")


if changed:

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Changes Saved")

else:

    print("No user needs reset today.")
