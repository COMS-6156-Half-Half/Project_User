import json
import boto3

client = boto3.client("sns")


def lambda_handler(event, context):
    print(event)
    print(event["Records"][0]["Sns"]["Message"])
    print(context)
    # TODO implement
    info = json.loads(event["Records"][0]["Sns"]["Message"])
    print(info["username"])

    SENDER = "yl4850@columbia.edu"
    RECIPIENT = "zt0202002@gmail.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "New User Registered"

    client = boto3.client("ses", region_name=AWS_REGION)
    message = f"New User Registered with username {info['username']} and assoicate email {info['email']}"
    CHARSET = "UTF-8"

    response = client.send_email(
        Destination={
            "ToAddresses": [
                RECIPIENT,
            ],
        },
        Message={
            "Body": {"Text": {"Data": message, "Charset": CHARSET}},
            "Subject": {
                "Charset": CHARSET,
                "Data": SUBJECT,
            },
        },
        Source=SENDER,
    )
    print("Message sent!")

    return {"statusCode": 200, "body": json.dumps(response)}
