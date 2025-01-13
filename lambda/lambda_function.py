import json
import boto3
import uuid

# DynamoDBテーブルを指定
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TodoTable')  # 作成済みのテーブル名 "TodoTable" を指定

def lambda_handler(event, context):
    """
    API Gatewayから呼び出されるLambda。
    DynamoDBへのデータ操作を行うサンプルです。
    - GET: 全ToDoを取得
    - POST: ToDoを新規作成
    """

    http_method = event.get("httpMethod")  # 例: "GET", "POST", etc.

    # POST時に送られるJSONボディを取得
    body_data = {}
    if event.get("body"):
        body_data = json.loads(event["body"])

    if http_method == "GET":
        # DynamoDBから全アイテムをスキャン（一覧取得）
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items),
            "headers": {"Content-Type": "application/json"}
        }

    elif http_method == "POST":
        # 新規のToDoを作成
        new_todo_id = str(uuid.uuid4())  # ランダムなIDを生成
        title = body_data.get("title", "")
        description = body_data.get("description", "")

        table.put_item(
            Item={
                "id": new_todo_id,
                "title": title,
                "description": description
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "New ToDo created",
                "id": new_todo_id,
                "title": title,
                "description": description
            }),
            "headers": {"Content-Type": "application/json"}
        }

    else:
        # それ以外のHTTPメソッドは対応しない
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Unsupported method: {http_method}"}),
            "headers": {"Content-Type": "application/json"}
        }
