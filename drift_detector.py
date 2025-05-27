import json

seen_keys = set()
with open("activity_logs.json") as f:
    for idx, line in enumerate(f, start=1):
        record = json.loads(line)
        keys = set(record.keys())

        # Detect brand-new fields
        new = keys - seen_keys
        if new:
            print(f" New field(s) at record {idx}: {new}")

        # (Optional) detect fields that were in seen_keys but missing here
        missing = seen_keys - keys
        if missing:
            print(f" Missing field(s) at record {idx}: {missing}")

        # Update your “universe” of keys
        seen_keys |= keys
