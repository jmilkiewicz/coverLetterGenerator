import json
from openai import OpenAI

from tune import tuneCoverLetter
from getApiKey import getApiKey


def handler(event, context):
    print(f"event is {event}")
    body = json.loads(event["body"])

    client = OpenAI(api_key=getApiKey())

    content = tuneCoverLetter(client, body)

    return build_response(content)


def build_response(content):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(content)
    }
