import json

def extract_paths(obj, prefix=""):
    """
    Recursively walk a JSON-like dict and return a set of all nested key-paths,
    using dot notation and collapsing list indices to “[]”.
    """
    paths = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            full = f"{prefix}.{k}" if prefix else k
            paths.add(full)
            paths |= extract_paths(v, full)
    elif isinstance(obj, list):
        for item in obj:
            # we collapse every list element into the same “[]” path
            list_prefix = f"{prefix}[]" if prefix else "[]"
            paths |= extract_paths(item, list_prefix)
    return paths

seen = set()

with open("activity_logs.json") as f:
    for idx, line in enumerate(f, start=1):
        record = json.loads(line)
        current = extract_paths(record)

        # Only check for brand‐new paths
        new = current - seen
        if new:
            print(f" New nested path(s) at record {idx}: {new}")

        # Update the seen set
        seen |= current
