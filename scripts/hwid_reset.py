import json
from datetime import datetime

FILE = "database/users.json"

today = datetime.utcnow().date()

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

changed = False

for owner in data.values():

    for username, user in owner.items():

        # Expiry users skip
        if user.get("expiryDate"):
            continue

        # Free users skip
        if user.get("isFreeUser") == True:
            continue

        hwid = user.get("hwid", "").strip()
        reset_date = user.get("hwid_reset_date", "").strip()

        if hwid == "":
            continue

        if reset_date == "":
            continue

        try:
            reset = datetime.strptime(reset_date, "%Y-%m-%d").date()

            if today >= reset:

                user["hwid"] = ""
                user["hwid_bind_date"] = ""
                user["hwid_reset_date"] = ""
                user["last_reset_date"] = today.strftime("%Y-%m-%d")

                changed = True

        except:
            pass

if changed:
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
