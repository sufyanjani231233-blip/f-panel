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

        # -----------------------------
        # Skip Free Users
        # -----------------------------
        if user.get("isFreeUser", False):
            print(f"[SKIP FREE] {owner_name} -> {username}")
            continue

        # -----------------------------
        # Skip Expired Users
        # -----------------------------
        expiry = str(user.get("expiryDate", "")).strip()

        if expiry != "":
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()

                # Agar account expire ho chuka hai
                if today > expiry_date:
                    print(f"[SKIP EXPIRED] {owner_name} -> {username}")
                    continue

            except Exception:
                print(f"[INVALID EXPIRY] {owner_name} -> {username}")
                continue

        # -----------------------------
        # Read HWID Data
        # -----------------------------
        hwid = str(user.get("hwid", "")).strip()
        reset_date = str(user.get("hwid_reset_date", "")).strip()

        # HWID ya Reset Date nahi hai
        if hwid == "" or reset_date == "":
            continue

        # -----------------------------
        # Check Reset Date
        # -----------------------------
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

            print(f"[INVALID RESET DATE] {owner_name} -> {username} : {e}")

# ------------------------------------
# Save File
# ------------------------------------

if changed:

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("===================================")
    print("Changes Saved Successfully")
    print("===================================")

else:

    print("===================================")
    print("No User Needs Reset Today")
    print("===================================")
