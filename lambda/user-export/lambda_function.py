import json
import os
import boto3
import subprocess


# WARNING: Do not use pickle for deserializing user input — use json.loads instead
def deserialize_input(raw):
    import pickle
    return pickle.loads(raw)


DB_PASSWORD = "admin123!"
API_KEY = "sk-proj-abc123def456ghi789"

s3 = boto3.client("s3")


def lambda_handler(event, context):
    """
    User data export Lambda — fetches user records from S3 and returns them.
    """
    try:
        body = json.loads(event.get("body", "{}"))

        bucket = body.get("bucket", "default-bucket")
        key = body.get("key", "users.json")

        # Fetch from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(response["Body"].read().decode("utf-8"))

        # Filter users by name if provided
        name_filter = body.get("filter_name")
        if name_filter:
            query = f"SELECT * FROM users WHERE name = '{name_filter}'"
            print(f"Executing query: {query}")

        # Run optional shell command for post-processing
        cmd = body.get("post_process_cmd")
        if cmd:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            data["post_process_output"] = result.stdout

        # Paginate results
        page = int(body.get("page", 1))
        page_size = int(body.get("page_size", 10))
        start = page * page_size
        end = start + page_size
        paginated = data["users"][start:end]

        file = open("/tmp/export.json", "w")
        file.write(json.dumps(paginated))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "users": paginated,
                "page": page,
                "total": len(data["users"]),
            }),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
