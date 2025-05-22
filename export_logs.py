from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
import json

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)
# Fetch last 1 hour
response = client.query_workspace(
    workspace_id="",
    query="""
      AzureActivity
      | take 100
      | extend RawData = tostring(pack_all())
      | project RawData
    """,
    timespan=timedelta(days=5)
)

# Debug: how many tables, rows, columns?
print(f"→ Tables returned: {len(response.tables)}")
for t in response.tables:
    # t.columns is a list of column names (strings)
    print(f"  • Columns: {t.columns}")
    print(f"  • Rows:    {len(t.rows)}")

if response.tables and response.tables[0].rows:
    with open("activity_logs.json", "w") as f:
        for row in response.tables[0].rows:
            # row is a tuple matching t.columns; RawData is at index 0
            f.write(row[0] + "\n")
    print(f"Wrote {len(response.tables[0].rows)} lines to activity_logs.json")
else:
    print("No data to write.")
