import json
import uuid
import boto3
from datetime import datetime

# DynamoDB setup
dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table = dynamodb.Table("StudentFormDB")  # DynamoDB table name

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # CORS preflight
    if method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    # POST → Save data
    if method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
            item = {
                "student_id": str(uuid.uuid4()),
                "name": body.get("name", ""),
                "email": body.get("email", ""),
                "mobile": body.get("mobile", ""),
                "slots": body.get("slots", []),
                "created_at": datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)
            return {"statusCode": 200, "headers": headers, "body": json.dumps({"success": True})}
        except Exception as e:
            return {"statusCode": 200, "headers": headers, "body": json.dumps({"success": False, "error": str(e)})}

    # GET → Fetch data
    if method == "GET":
        try:
            response = table.scan()
            items = response.get("Items", [])
            if not isinstance(items, list):
                items = []
            return {"statusCode": 200, "headers": headers, "body": json.dumps(items)}
        except Exception as e:
            return {"statusCode": 200, "headers": headers, "body": json.dumps([])}

    # Any other method
    return {"statusCode": 405, "headers": headers, "body": json.dumps([])}
